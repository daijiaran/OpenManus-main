#!/usr/bin/env python3
"""
OpenManus Desktop GUI Application - Enhanced Version
增强版桌面图形化界面，包含更好的日志集成和错误处理
"""

import sys
import asyncio
import io
from pathlib import Path
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel, QCheckBox,
    QMenuBar, QMenu, QStatusBar, QMessageBox, QTabWidget,
    QFileDialog, QProgressBar
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject, QTimer
from PyQt6.QtGui import QTextCursor, QFont, QColor, QTextCharFormat, QAction
import qasync
from qasync import QEventLoop, asyncSlot

from app.agent.manus import Manus
from app.schema import AgentState, Memory
from loguru import logger


class LogCapture(io.StringIO):
    """捕获日志输出"""
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def write(self, message):
        if message.strip():
            self.callback(message)
        return len(message)


class ManusGUI(QMainWindow):
    """OpenManus 增强版 GUI 主窗口"""
    
    log_signal = pyqtSignal(str, str)  # (message, level)
    status_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.agent = None
        self.is_running = False
        self.task_count = 0
        
        self.init_ui()
        self.setup_logger()
        self.setup_connections()
        
        # 异步初始化
        asyncio.ensure_future(self.async_init())

    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("OpenManus Desktop - Enhanced")
        self.setMinimumSize(1000, 750)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
            }
            QPushButton {
                background-color: #0066cc;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0052a3;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)

        # 中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # 创建菜单
        self.create_menus()

        # 标题区域
        title_layout = QHBoxLayout()
        title_label = QLabel("🤖 OpenManus AI Agent")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        self.status_indicator = QLabel("⚪ 未初始化")
        self.status_indicator.setFont(QFont("Arial", 10))
        title_layout.addWidget(self.status_indicator)
        
        main_layout.addLayout(title_layout)

        # Tab 控件
        self.tabs = QTabWidget()
        
        # Tab 1: 对话界面
        chat_tab = QWidget()
        chat_layout = QVBoxLayout(chat_tab)
        
        # 对话显示区域
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Consolas", 10))
        chat_layout.addWidget(self.chat_display)
        
        # 输入区域
        input_container = QWidget()
        input_layout = QVBoxLayout(input_container)
        
        # 文本输入
        input_row = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("输入您的任务指令...")
        self.input_field.setFont(QFont("Arial", 11))
        self.input_field.returnPressed.connect(self.on_send_clicked)
        input_row.addWidget(self.input_field)
        
        self.send_btn = QPushButton("发送 ▶")
        self.send_btn.setMinimumWidth(100)
        self.send_btn.clicked.connect(self.on_send_clicked)
        input_row.addWidget(self.send_btn)
        
        input_layout.addLayout(input_row)
        
        # 控制按钮行
        control_row = QHBoxLayout()
        
        self.keep_memory_cb = QCheckBox("保持对话记忆")
        self.keep_memory_cb.setChecked(False)
        control_row.addWidget(self.keep_memory_cb)
        
        control_row.addStretch()
        
        self.clear_btn = QPushButton("清空对话")
        self.clear_btn.setStyleSheet("background-color: #666;")
        self.clear_btn.clicked.connect(self.clear_chat)
        control_row.addWidget(self.clear_btn)
        
        self.stop_btn = QPushButton("停止任务")
        self.stop_btn.setStyleSheet("background-color: #cc0000;")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_task)
        control_row.addWidget(self.stop_btn)
        
        input_layout.addLayout(control_row)
        chat_layout.addWidget(input_container)
        
        self.tabs.addTab(chat_tab, "💬 对话")
        
        # Tab 2: 日志界面
        log_tab = QWidget()
        log_layout = QVBoxLayout(log_tab)
        
        log_controls = QHBoxLayout()
        log_controls.addWidget(QLabel("执行日志:"))
        log_controls.addStretch()
        
        clear_log_btn = QPushButton("清空日志")
        clear_log_btn.setStyleSheet("background-color: #666;")
        clear_log_btn.clicked.connect(lambda: self.log_display.clear())
        log_controls.addWidget(clear_log_btn)
        
        log_layout.addLayout(log_controls)
        
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setFont(QFont("Consolas", 9))
        log_layout.addWidget(self.log_display)
        
        self.tabs.addTab(log_tab, "📋 日志")
        
        main_layout.addWidget(self.tabs)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(False)
        main_layout.addWidget(self.progress_bar)

        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_status("就绪")

    def create_menus(self):
        """创建菜单栏"""
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu("文件")
        
        export_chat_action = QAction("导出对话记录", self)
        export_chat_action.triggered.connect(self.export_chat)
        file_menu.addAction(export_chat_action)
        
        export_log_action = QAction("导出日志", self)
        export_log_action.triggered.connect(self.export_log)
        file_menu.addAction(export_log_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 编辑菜单
        edit_menu = menubar.addMenu("编辑")
        
        clear_chat_action = QAction("清空对话", self)
        clear_chat_action.triggered.connect(self.clear_chat)
        edit_menu.addAction(clear_chat_action)
        
        clear_log_action = QAction("清空日志", self)
        clear_log_action.triggered.connect(lambda: self.log_display.clear())
        edit_menu.addAction(clear_log_action)

        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
        
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        docs_action = QAction("使用文档", self)
        docs_action.triggered.connect(self.show_docs)
        help_menu.addAction(docs_action)

    def setup_logger(self):
        """设置日志捕获"""
        # 移除默认处理器
        logger.remove()
        
        # 添加自定义处理器
        logger.add(
            lambda msg: self.log_signal.emit(msg, "INFO"),
            format="{time:HH:mm:ss} | {level} | {message}",
            level="DEBUG"
        )

    def setup_connections(self):
        """设置信号连接"""
        self.log_signal.connect(self.append_log)
        self.status_signal.connect(self.update_status)

    @asyncSlot()
    async def async_init(self):
        """异步初始化"""
        try:
            self.append_log("🚀 正在初始化 OpenManus Agent...", "INFO")
            self.status_indicator.setText("🟡 初始化中...")
            
            self.agent = await Manus.create()
            
            self.append_log("✅ Agent 初始化成功!", "INFO")
            self.status_indicator.setText("🟢 就绪")
            self.append_chat_system("欢迎使用 OpenManus Desktop! 请输入您的任务指令。")
            
        except Exception as e:
            self.append_log(f"❌ 初始化失败: {str(e)}", "ERROR")
            self.status_indicator.setText("🔴 初始化失败")
            QMessageBox.critical(self, "错误", f"Agent 初始化失败:\n{str(e)}")

    @asyncSlot()
    async def on_send_clicked(self):
        """发送按钮点击处理"""
        prompt = self.input_field.text().strip()
        if not prompt:
            return

        if self.is_running:
            QMessageBox.warning(self, "警告", "当前有任务正在执行，请等待完成")
            return

        if not self.agent:
            QMessageBox.warning(self, "警告", "Agent 未初始化，请稍候")
            return

        # 清空输入框
        self.input_field.clear()
        
        # 显示用户消息
        self.append_chat_user(prompt)
        
        # 更新 UI 状态
        self.is_running = True
        self.send_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_indicator.setText("🟡 执行中...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # 不确定进度
        
        self.task_count += 1
        
        try:
            # 重置 agent 状态
            self.agent.state = AgentState.IDLE
            self.agent.current_step = 0
            
            # 清除记忆（如果需要）
            if not self.keep_memory_cb.isChecked():
                self.agent.memory = Memory()
                self.append_log("🧹 已清除对话记忆", "DEBUG")
            
            self.append_log(f"📝 开始执行任务 #{self.task_count}: {prompt[:50]}...", "INFO")
            
            # 执行任务
            await self.agent.run(prompt)
            
            self.append_log(f"✅ 任务 #{self.task_count} 完成", "INFO")
            self.append_chat_system("任务执行完成")
            
        except Exception as e:
            error_msg = f"❌ 任务执行失败: {str(e)}"
            self.append_log(error_msg, "ERROR")
            self.append_chat_system(f"错误: {str(e)}")
            QMessageBox.critical(self, "执行错误", str(e))
            
        finally:
            # 恢复 UI 状态
            self.is_running = False
            self.send_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.status_indicator.setText("🟢 就绪")
            self.progress_bar.setVisible(False)
            self.update_status("就绪")

    def stop_task(self):
        """停止当前任务"""
        QMessageBox.information(
            self, "提示",
            "任务停止功能需要在 Agent 层面实现中断机制。\n"
            "当前版本暂不支持，请等待任务完成。"
        )

    def clear_chat(self):
        """清空对话"""
        reply = QMessageBox.question(
            self, "确认",
            "确定要清空对话历史吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.chat_display.clear()
            self.append_log("🧹 对话历史已清空", "INFO")

    def append_chat_user(self, message: str):
        """添加用户消息"""
        self._append_chat("👤 用户", message, "#0066CC")

    def append_chat_system(self, message: str):
        """添加系统消息"""
        self._append_chat("🤖 Manus", message, "#006600")

    def _append_chat(self, sender: str, message: str, color: str):
        """添加聊天消息（内部方法）"""
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        # 时间戳
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # 分隔线
        fmt_separator = QTextCharFormat()
        fmt_separator.setForeground(QColor("#CCCCCC"))
        cursor.setCharFormat(fmt_separator)
        cursor.insertText(f"\n{'─' * 80}\n")
        
        # 发送者和时间
        fmt_header = QTextCharFormat()
        fmt_header.setForeground(QColor(color))
        fmt_header.setFontWeight(QFont.Weight.Bold)
        cursor.setCharFormat(fmt_header)
        cursor.insertText(f"{sender} [{timestamp}]\n")
        
        # 消息内容
        fmt_content = QTextCharFormat()
        fmt_content.setForeground(QColor("#000000"))
        cursor.setCharFormat(fmt_content)
        cursor.insertText(f"{message}\n")
        
        self.chat_display.setTextCursor(cursor)
        self.chat_display.ensureCursorVisible()

    def append_log(self, message: str, level: str = "INFO"):
        """添加日志"""
        cursor = self.log_display.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        # 根据级别设置颜色
        color_map = {
            "ERROR": "#CC0000",
            "WARNING": "#FF8800",
            "DEBUG": "#888888",
            "INFO": "#000000"
        }
        
        fmt = QTextCharFormat()
        # 从消息中提取级别
        for lvl, color in color_map.items():
            if lvl in message:
                fmt.setForeground(QColor(color))
                break
        else:
            fmt.setForeground(QColor(color_map.get(level, "#000000")))
        
        cursor.setCharFormat(fmt)
        cursor.insertText(f"{message}\n")
        
        self.log_display.setTextCursor(cursor)
        self.log_display.ensureCursorVisible()

    def update_status(self, status: str):
        """更新状态栏"""
        status_text = f"状态: {status} | 任务计数: {self.task_count}"
        if self.agent:
            step = getattr(self.agent, 'current_step', 0)
            status_text += f" | 当前步骤: {step}"
        self.status_bar.showMessage(status_text)

    def export_chat(self):
        """导出对话记录"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出对话记录",
            f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "文本文件 (*.txt);;所有文件 (*)"
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.chat_display.toPlainText())
                self.append_log(f"✅ 对话已导出: {file_path}", "INFO")
                QMessageBox.information(self, "成功", "对话记录已成功导出")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出失败:\n{str(e)}")

    def export_log(self):
        """导出日志"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出日志",
            f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "文本文件 (*.txt);;所有文件 (*)"
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.log_display.toPlainText())
                self.append_log(f"✅ 日志已导出: {file_path}", "INFO")
                QMessageBox.information(self, "成功", "日志已成功导出")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出失败:\n{str(e)}")

    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(
            self, "关于 OpenManus Desktop",
            "<h2>OpenManus Desktop GUI</h2>"
            "<p><b>版本:</b> 1.0.0 Enhanced</p>"
            "<p><b>描述:</b> 基于 PyQt6 的桌面图形化界面</p>"
            "<p><b>项目:</b> <a href='https://github.com/FoundationAgents/OpenManus'>"
            "OpenManus</a></p>"
            "<p><b>许可证:</b> MIT</p>"
            "<p><b>作者:</b> OpenManus Team</p>"
        )

    def show_docs(self):
        """显示使用文档"""
        QMessageBox.information(
            self, "使用文档",
            "<h3>快速开始</h3>"
            "<ol>"
            "<li>在输入框中输入您的任务指令</li>"
            "<li>点击「发送」按钮或按 Enter 键</li>"
            "<li>等待 Agent 执行任务</li>"
            "<li>查看对话和日志标签页了解执行详情</li>"
            "</ol>"
            "<h3>功能说明</h3>"
            "<ul>"
            "<li><b>保持对话记忆:</b> 勾选后会保留之前的对话上下文</li>"
            "<li><b>清空对话:</b> 清除对话历史显示</li>"
            "<li><b>停止任务:</b> 尝试中断当前任务（开发中）</li>"
            "<li><b>导出功能:</b> 可导出对话记录和日志到文件</li>"
            "</ul>"
        )

    @asyncSlot()
    async def closeEvent(self, event):
        """关闭事件"""
        if self.is_running:
            reply = QMessageBox.question(
                self, "确认退出",
                "当前有任务正在执行，确定要退出吗？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return

        # 清理资源
        if self.agent:
            try:
                self.append_log("🧹 正在清理资源...", "INFO")
                await self.agent.cleanup()
                self.append_log("✨ 清理完成", "INFO")
            except Exception as e:
                self.append_log(f"⚠️ 清理时出错: {str(e)}", "WARNING")

        event.accept()


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setApplicationName("OpenManus Desktop")
    
    # 设置异步事件循环
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    # 创建并显示主窗口
    window = ManusGUI()
    window.show()

    # 运行事件循环
    with loop:
        loop.run_forever()


if __name__ == "__main__":
    main()

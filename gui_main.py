#!/usr/bin/env python3
"""
OpenManus Desktop GUI Application
基于 PyQt6 的桌面图形化界面
"""

import sys
import asyncio
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel, QCheckBox,
    QMenuBar, QMenu, QStatusBar, QSplitter, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QObject
from PyQt6.QtGui import QTextCursor, QFont, QColor, QTextCharFormat, QAction
import qasync
from qasync import QEventLoop, asyncSlot

from app.agent.manus import Manus
from app.schema import AgentState, Memory
from app.logger import logger


class LogHandler(QObject):
    """日志处理器，将日志输出重定向到 GUI"""
    log_signal = pyqtSignal(str, str)  # (message, level)

    def __init__(self):
        super().__init__()

    def write(self, message):
        """处理日志消息"""
        if message.strip():
            # 简单的日志级别检测
            level = "INFO"
            if "ERROR" in message or "Exception" in message:
                level = "ERROR"
            elif "WARNING" in message or "⚠️" in message:
                level = "WARNING"
            elif "DEBUG" in message:
                level = "DEBUG"
            self.log_signal.emit(message, level)


class ManusWorker(QObject):
    """Manus Agent 工作线程"""
    finished = pyqtSignal()
    error = pyqtSignal(str)
    log_message = pyqtSignal(str, str)  # (message, level)

    def __init__(self):
        super().__init__()
        self.agent = None
        self.is_running = False

    async def initialize_agent(self):
        """初始化 Manus Agent"""
        try:
            self.agent = await Manus.create()
            self.log_message.emit("✅ Manus Agent 初始化成功", "INFO")
        except Exception as e:
            self.error.emit(f"Agent 初始化失败: {str(e)}")
            raise

    async def run_task(self, prompt: str, keep_memory: bool = False):
        """执行任务"""
        if not self.agent:
            await self.initialize_agent()

        try:
            self.is_running = True
            
            # 重置 agent 状态
            self.agent.state = AgentState.IDLE
            self.agent.current_step = 0

            # 清除记忆（如果需要）
            if not keep_memory:
                self.agent.memory = Memory()
                self.log_message.emit("🧹 已清除对话记忆", "DEBUG")
            else:
                self.log_message.emit("💾 保持对话记忆", "DEBUG")

            self.log_message.emit(f"📝 开始处理任务: {prompt}", "INFO")
            
            # 执行任务
            await self.agent.run(prompt)
            
            self.log_message.emit("✅ 任务处理完成", "INFO")
            self.finished.emit()
            
        except Exception as e:
            self.error.emit(f"任务执行错误: {str(e)}")
        finally:
            self.is_running = False

    async def cleanup(self):
        """清理资源"""
        if self.agent:
            try:
                await self.agent.cleanup()
                self.log_message.emit("🧹 资源清理完成", "INFO")
            except Exception as e:
                self.error.emit(f"清理失败: {str(e)}")


class ConfigDialog(QWidget):
    """配置对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("配置")
        self.setMinimumSize(500, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        info_label = QLabel("配置文件位置: config/config.toml")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        instruction = QLabel(
            "请直接编辑 config/config.toml 文件来修改配置。\n"
            "主要配置项包括：\n"
            "- LLM 模型和 API Key\n"
            "- Base URL\n"
            "- 温度和最大 tokens\n"
            "- 其他高级选项"
        )
        instruction.setWordWrap(True)
        layout.addWidget(instruction)
        
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self.worker = ManusWorker()
        self.init_ui()
        self.setup_connections()
        
        # 异步初始化 agent
        asyncio.ensure_future(self.initialize_agent())

    def init_ui(self):
        """初始化 UI"""
        self.setWindowTitle("OpenManus Desktop")
        self.setMinimumSize(900, 700)

        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 创建菜单栏
        self.create_menu_bar()

        # 对话历史区域
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Consolas", 10))
        main_layout.addWidget(QLabel("对话历史:"))
        main_layout.addWidget(self.chat_display, stretch=3)

        # 日志区域
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setFont(QFont("Consolas", 9))
        self.log_display.setMaximumHeight(200)
        main_layout.addWidget(QLabel("执行日志:"))
        main_layout.addWidget(self.log_display, stretch=1)

        # 输入区域
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("输入您的任务...")
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)

        # 控制按钮
        self.send_btn = QPushButton("发送")
        self.send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_btn)

        self.stop_btn = QPushButton("停止")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_task)
        input_layout.addWidget(self.stop_btn)

        self.clear_btn = QPushButton("清空对话")
        self.clear_btn.clicked.connect(self.clear_chat)
        input_layout.addWidget(self.clear_btn)

        main_layout.addLayout(input_layout)

        # 选项区域
        options_layout = QHBoxLayout()
        self.keep_memory_cb = QCheckBox("保持记忆")
        self.keep_memory_cb.setChecked(False)
        options_layout.addWidget(self.keep_memory_cb)
        options_layout.addStretch()
        main_layout.addLayout(options_layout)

        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_status("就绪", "idle")

    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu("文件")
        
        export_action = QAction("导出对话", self)
        export_action.triggered.connect(self.export_chat)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 配置菜单
        config_menu = menubar.addMenu("配置")
        
        settings_action = QAction("设置", self)
        settings_action.triggered.connect(self.show_config)
        config_menu.addAction(settings_action)

        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
        
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def setup_connections(self):
        """设置信号连接"""
        self.worker.log_message.connect(self.append_log)
        self.worker.finished.connect(self.on_task_finished)
        self.worker.error.connect(self.on_task_error)

    @asyncSlot()
    async def initialize_agent(self):
        """异步初始化 agent"""
        try:
            self.append_log("🚀 正在初始化 Manus Agent...", "INFO")
            await self.worker.initialize_agent()
        except Exception as e:
            self.append_log(f"❌ 初始化失败: {str(e)}", "ERROR")
            QMessageBox.critical(self, "错误", f"Agent 初始化失败:\n{str(e)}")

    @asyncSlot()
    async def send_message(self):
        """发送消息"""
        prompt = self.input_field.text().strip()
        if not prompt:
            return

        if self.worker.is_running:
            QMessageBox.warning(self, "警告", "当前有任务正在执行，请等待完成或停止后再试")
            return

        # 显示用户消息
        self.append_chat_message("用户", prompt, is_user=True)
        self.input_field.clear()

        # 更新状态
        self.update_status("执行中", "running")
        self.send_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

        # 执行任务
        keep_memory = self.keep_memory_cb.isChecked()
        try:
            await self.worker.run_task(prompt, keep_memory)
        except Exception as e:
            self.append_log(f"❌ 执行错误: {str(e)}", "ERROR")

    def stop_task(self):
        """停止当前任务"""
        # TODO: 实现任务中断逻辑
        self.append_log("⚠️ 停止功能暂未实现", "WARNING")

    def clear_chat(self):
        """清空对话历史"""
        reply = QMessageBox.question(
            self, "确认", "确定要清空对话历史吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.chat_display.clear()
            self.append_log("🧹 对话历史已清空", "INFO")

    def append_chat_message(self, sender: str, message: str, is_user: bool = False):
        """添加聊天消息"""
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)

        # 设置格式
        fmt = QTextCharFormat()
        if is_user:
            fmt.setForeground(QColor("#0066CC"))
        else:
            fmt.setForeground(QColor("#006600"))
        
        cursor.setCharFormat(fmt)
        cursor.insertText(f"\n{'='*60}\n")
        cursor.insertText(f"{'👤' if is_user else '🤖'} {sender}: {message}\n")
        
        self.chat_display.setTextCursor(cursor)
        self.chat_display.ensureCursorVisible()

    def append_log(self, message: str, level: str = "INFO"):
        """添加日志消息"""
        cursor = self.log_display.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)

        # 根据级别设置颜色
        fmt = QTextCharFormat()
        if level == "ERROR":
            fmt.setForeground(QColor("#CC0000"))
        elif level == "WARNING":
            fmt.setForeground(QColor("#FF8800"))
        elif level == "DEBUG":
            fmt.setForeground(QColor("#888888"))
        else:
            fmt.setForeground(QColor("#000000"))

        cursor.setCharFormat(fmt)
        cursor.insertText(f"{message}\n")
        
        self.log_display.setTextCursor(cursor)
        self.log_display.ensureCursorVisible()

    def update_status(self, status: str, state: str):
        """更新状态栏"""
        status_text = f"状态: {status}"
        if hasattr(self.worker, 'agent') and self.worker.agent:
            status_text += f" | 步骤: {getattr(self.worker.agent, 'current_step', 0)}"
        self.status_bar.showMessage(status_text)

    def on_task_finished(self):
        """任务完成回调"""
        self.update_status("就绪", "idle")
        self.send_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.append_chat_message("Manus", "任务已完成", is_user=False)

    def on_task_error(self, error_msg: str):
        """任务错误回调"""
        self.update_status("错误", "error")
        self.send_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.append_log(f"❌ {error_msg}", "ERROR")
        self.append_chat_message("系统", f"错误: {error_msg}", is_user=False)

    def show_config(self):
        """显示配置对话框"""
        config_dialog = ConfigDialog(self)
        config_dialog.show()

    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(
            self, "关于 OpenManus",
            "OpenManus Desktop GUI\n\n"
            "版本: 1.0.0\n"
            "基于 PyQt6 构建的桌面图形化界面\n\n"
            "项目地址: https://github.com/FoundationAgents/OpenManus\n"
            "许可证: MIT"
        )

    def export_chat(self):
        """导出对话记录"""
        from PyQt6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出对话", "", "文本文件 (*.txt);;所有文件 (*)"
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.chat_display.toPlainText())
                self.append_log(f"✅ 对话已导出到: {file_path}", "INFO")
                QMessageBox.information(self, "成功", "对话记录已成功导出")
            except Exception as e:
                self.append_log(f"❌ 导出失败: {str(e)}", "ERROR")
                QMessageBox.critical(self, "错误", f"导出失败:\n{str(e)}")

    @asyncSlot()
    async def closeEvent(self, event):
        """关闭事件处理"""
        if self.worker.is_running:
            reply = QMessageBox.question(
                self, "确认退出",
                "当前有任务正在执行，确定要退出吗？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return

        # 清理资源
        self.append_log("🧹 正在清理资源...", "INFO")
        await self.worker.cleanup()
        event.accept()


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置事件循环
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    # 创建主窗口
    window = MainWindow()
    window.show()

    # 运行事件循环
    with loop:
        loop.run_forever()


if __name__ == "__main__":
    main()

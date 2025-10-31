# OpenManus Desktop GUI 使用文档

## 简介

OpenManus Desktop GUI 是为 OpenManus 项目开发的桌面图形化界面，提供了友好的用户交互体验，让您无需使用命令行即可轻松使用 OpenManus AI Agent。

## 功能特性

### 核心功能

- **交互式对话界面**：直观的聊天式界面，支持连续对话
- **实时日志显示**：独立的日志标签页，实时显示 Agent 执行详情
- **记忆管理**：可选择保持或清除对话上下文
- **任务控制**：发送、停止、清空等操作
- **数据导出**：支持导出对话记录和日志到文件
- **状态监控**：实时显示 Agent 状态、任务计数、执行步骤等信息

### 界面组成

#### 1. 对话标签页
- **对话历史区域**：显示用户输入和 Agent 响应
- **输入框**：输入任务指令
- **发送按钮**：提交任务（或按 Enter 键）
- **控制按钮**：
  - 保持对话记忆：勾选后保留对话上下文
  - 清空对话：清除对话历史显示
  - 停止任务：中断当前执行（开发中）

#### 2. 日志标签页
- **日志显示区域**：显示详细的执行日志
- **清空日志按钮**：清除日志显示

#### 3. 菜单栏
- **文件菜单**：
  - 导出对话记录
  - 导出日志
  - 退出
- **编辑菜单**：
  - 清空对话
  - 清空日志
- **帮助菜单**：
  - 关于
  - 使用文档

#### 4. 状态栏
显示当前状态、任务计数、执行步骤等信息

## 安装说明

### 前置要求

- Python 3.12 或更高版本
- 已安装 OpenManus 项目的基础依赖

### 安装步骤

#### 方法 1: 使用 pip

```bash
# 进入项目目录
cd OpenManus

# 安装 GUI 依赖
pip install -r requirements-gui.txt
```

#### 方法 2: 使用 uv（推荐）

```bash
# 进入项目目录
cd OpenManus

# 安装 GUI 依赖
uv pip install -r requirements-gui.txt
```

### 依赖说明

GUI 版本额外需要以下依赖：
- **PyQt6** (>=6.6.0): Qt 6 的 Python 绑定，提供 GUI 组件
- **qasync** (>=0.27.0): PyQt 和 asyncio 的集成库

## 使用方法

### 启动应用

#### Linux/macOS

```bash
# 方法 1: 使用启动脚本
./start_gui.sh

# 方法 2: 直接运行（推荐增强版）
python3 gui_enhanced.py

# 方法 3: 运行基础版
python3 gui_main.py
```

#### Windows

```batch
REM 方法 1: 使用启动脚本
start_gui.bat

REM 方法 2: 直接运行（推荐增强版）
python gui_enhanced.py

REM 方法 3: 运行基础版
python gui_main.py
```

### 配置

在首次使用前，请确保已配置 `config/config.toml` 文件：

```toml
[llm]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."  # 您的 API Key
max_tokens = 4096
temperature = 0.0
```

### 基本操作流程

1. **启动应用**
   - 运行启动脚本或直接执行 Python 文件
   - 等待 Agent 初始化完成（状态指示器变为绿色）

2. **输入任务**
   - 在输入框中输入您的任务指令
   - 例如："帮我分析一下这个数据集"

3. **发送任务**
   - 点击「发送」按钮或按 Enter 键
   - 观察对话区域的 Agent 响应

4. **查看执行详情**
   - 切换到「日志」标签页查看详细执行日志
   - 状态栏显示当前执行状态

5. **管理对话**
   - 勾选「保持对话记忆」以保留上下文
   - 点击「清空对话」清除历史记录

6. **导出数据**
   - 菜单 → 文件 → 导出对话记录/导出日志
   - 选择保存位置

## 版本说明

### gui_main.py（基础版）
- 基本的 GUI 功能
- 简单的日志集成
- 适合快速测试

### gui_enhanced.py（增强版，推荐）
- 更美观的界面设计
- 更好的日志捕获和显示
- 标签页布局
- 丰富的状态信息
- 完善的错误处理
- 推荐日常使用

## 技术架构

### 技术栈
- **PyQt6**: 跨平台 GUI 框架
- **qasync**: 异步支持
- **asyncio**: 异步任务执行
- **loguru**: 日志处理

### 异步集成
使用 `qasync` 库实现 PyQt6 事件循环与 asyncio 的集成，确保 GUI 在执行异步任务时保持响应。

### 日志捕获
通过自定义 loguru 处理器，将 Agent 执行日志实时重定向到 GUI 显示。

## 常见问题

### Q1: 启动时提示 PyQt6 未安装
**A**: 运行 `pip install -r requirements-gui.txt` 安装依赖

### Q2: Agent 初始化失败
**A**: 检查 `config/config.toml` 配置是否正确，特别是 API Key

### Q3: 任务执行时界面卡死
**A**: 这是正常现象，Agent 在后台执行任务。增强版已优化此问题。

### Q4: 如何停止正在执行的任务
**A**: 当前版本暂不支持任务中断，请等待任务完成或重启应用

### Q5: 日志显示不完整
**A**: 切换到「日志」标签页查看完整日志，或导出日志文件

## 开发说明

### 项目结构

```
OpenManus/
├── gui_main.py           # 基础版 GUI
├── gui_enhanced.py       # 增强版 GUI（推荐）
├── requirements-gui.txt  # GUI 依赖
├── start_gui.sh         # Linux/macOS 启动脚本
├── start_gui.bat        # Windows 启动脚本
├── GUI_DESIGN.md        # 设计文档
└── GUI_README.md        # 使用文档（本文件）
```

### 扩展开发

如需自定义 GUI，可以基于现有代码进行修改：

1. **修改界面布局**：编辑 `init_ui()` 方法
2. **添加新功能**：创建新的槽函数并连接信号
3. **自定义样式**：修改 `setStyleSheet()` 中的 CSS
4. **集成新工具**：在 `ManusWorker` 中添加新方法

### 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License - 与 OpenManus 项目保持一致

## 致谢

- OpenManus 团队
- PyQt6 项目
- qasync 项目

## 联系方式

- 项目主页: https://github.com/FoundationAgents/OpenManus
- 问题反馈: https://github.com/FoundationAgents/OpenManus/issues

---

**享受使用 OpenManus Desktop GUI！** 🚀

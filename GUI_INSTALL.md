# OpenManus Desktop GUI 安装指南

## 快速开始

本指南将帮助您在本地环境中安装和运行 OpenManus Desktop GUI。

## 系统要求

- **操作系统**: Windows 10+, macOS 10.14+, 或 Linux (Ubuntu 20.04+)
- **Python**: 3.12 或更高版本
- **内存**: 至少 4GB RAM
- **网络**: 需要互联网连接（用于 API 调用）

## 安装步骤

### 第一步：克隆项目

```bash
git clone https://github.com/FoundationAgents/OpenManus.git
cd OpenManus
```

### 第二步：创建虚拟环境（推荐）

#### 使用 conda

```bash
conda create -n open_manus python=3.12
conda activate open_manus
```

#### 使用 venv

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate  # Windows
```

#### 使用 uv（推荐，更快）

```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh  # Linux/macOS
# 或访问 https://github.com/astral-sh/uv 查看 Windows 安装方法

# 创建虚拟环境
uv venv --python 3.12
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate  # Windows
```

### 第三步：安装依赖

#### 方法 1: 安装所有依赖（包括 GUI）

```bash
# 使用 pip
pip install -r requirements-gui.txt

# 或使用 uv（更快）
uv pip install -r requirements-gui.txt
```

#### 方法 2: 分步安装

```bash
# 1. 安装基础依赖
pip install -r requirements.txt

# 2. 安装 GUI 依赖
pip install PyQt6>=6.6.0 qasync>=0.27.0
```

### 第四步：配置 API

1. 复制配置示例文件：

```bash
cp config/config.example.toml config/config.toml
```

2. 编辑 `config/config.toml`，填入您的 API 信息：

```toml
[llm]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-your-api-key-here"  # 替换为您的实际 API Key
max_tokens = 4096
temperature = 0.0
```

### 第五步：（可选）安装浏览器自动化工具

如果需要使用浏览器自动化功能：

```bash
playwright install
```

## 启动 GUI

### Linux/macOS

```bash
# 方法 1: 使用启动脚本（推荐）
./start_gui.sh

# 方法 2: 直接运行增强版（推荐）
python3 gui_enhanced.py

# 方法 3: 运行基础版
python3 gui_main.py
```

### Windows

```batch
REM 方法 1: 使用启动脚本（推荐）
start_gui.bat

REM 方法 2: 直接运行增强版（推荐）
python gui_enhanced.py

REM 方法 3: 运行基础版
python gui_main.py
```

## 验证安装

运行测试脚本检查安装是否成功：

```bash
python3 test_gui.py
```

成功的输出应该显示所有测试通过：

```
============================================================
测试总结
============================================================
依赖导入: ✅ 通过
文件结构: ✅ 通过
语法检查: ✅ 通过
配置文件: ✅ 通过

============================================================
🎉 所有测试通过! GUI 已准备就绪。
```

## 常见问题

### 问题 1: PyQt6 安装失败

**症状**: `pip install PyQt6` 报错

**解决方案**:

```bash
# 更新 pip
pip install --upgrade pip

# 重新安装
pip install PyQt6

# 如果还是失败，尝试指定版本
pip install PyQt6==6.6.0
```

### 问题 2: 找不到 config.toml

**症状**: 启动时提示配置文件不存在

**解决方案**:

```bash
# 复制示例配置
cp config/config.example.toml config/config.toml

# 编辑配置文件
nano config/config.toml  # 或使用其他编辑器
```

### 问题 3: API Key 无效

**症状**: Agent 初始化失败，提示 API 错误

**解决方案**:
1. 检查 `config/config.toml` 中的 `api_key` 是否正确
2. 确认 API Key 有效且有足够的配额
3. 检查 `base_url` 是否正确

### 问题 4: 导入 app.agent.manus 失败

**症状**: `ModuleNotFoundError: No module named 'app'`

**解决方案**:
确保在项目根目录运行 GUI：

```bash
cd /path/to/OpenManus
python3 gui_enhanced.py
```

### 问题 5: qasync 相关错误

**症状**: 启动时提示 qasync 错误

**解决方案**:

```bash
# 重新安装 qasync
pip uninstall qasync
pip install qasync>=0.27.0
```

### 问题 6: Linux 下缺少 Qt 平台插件

**症状**: `qt.qpa.plugin: Could not load the Qt platform plugin`

**解决方案**:

```bash
# Ubuntu/Debian
sudo apt-get install libxcb-xinerama0 libxcb-cursor0

# Fedora
sudo dnf install xcb-util-cursor
```

## 依赖列表

### 核心依赖（requirements.txt）
- pydantic ~= 2.10.6
- openai ~= 1.66.3
- tenacity ~= 9.0.0
- loguru ~= 0.7.3
- 其他（见 requirements.txt）

### GUI 依赖（requirements-gui.txt）
- PyQt6 >= 6.6.0
- qasync >= 0.27.0

## 开发环境设置

如果您想参与 GUI 开发：

```bash
# 安装开发依赖
pip install -r requirements.txt
pip install -r requirements-gui.txt

# 安装代码格式化工具
pip install black flake8 mypy

# 运行代码检查
flake8 gui_main.py gui_enhanced.py
black --check gui_main.py gui_enhanced.py
```

## 卸载

如果需要卸载 GUI 组件：

```bash
# 卸载 GUI 依赖
pip uninstall PyQt6 qasync

# 删除 GUI 文件
rm gui_main.py gui_enhanced.py
rm start_gui.sh start_gui.bat
rm requirements-gui.txt
rm GUI_*.md
```

## 下一步

安装完成后，请阅读 [GUI_README.md](GUI_README.md) 了解如何使用 GUI。

## 获取帮助

- **项目主页**: https://github.com/FoundationAgents/OpenManus
- **问题反馈**: https://github.com/FoundationAgents/OpenManus/issues
- **讨论区**: https://github.com/FoundationAgents/OpenManus/discussions

---

祝您使用愉快！🚀

# 运行时错误解决方案

## 错误分析

### 错误信息
```
ModuleNotFoundError: No module named 'pydantic'
Warning: Unsupported Python version 3.14.0.final.0, please use 3.11-3.13
```

### 问题根源

1. **Python 版本不匹配**：
   - 你使用 `C:/Python314/python.exe`（Python 3.14）运行脚本
   - 但依赖包安装在 **Python 3.13** 环境中
   - Python 3.14 中**没有安装任何依赖包**

2. **太多新的 Python 版本**：
   - 警告明确提示：只支持 Python 3.11-3.13
   - Python 3.14 太新，可能不被支持

### 检查结果

✅ **Python 3.13**: 已安装 `pydantic 2.10.6` 等依赖
❌ **Python 3.14**: 没有安装任何依赖包

## 解决方案

### 方案 1: 使用 Python 3.13 运行（推荐）

```powershell
# 方法 1: 使用 Python Launcher
py -3.13 main.py

# 方法 2: 直接使用 Python 3.13 的完整路径
C:\Users\DAI\AppData\Local\Programs\Python\Python313\python.exe main.py

# 方法 3: 激活 Python 3.13 的虚拟环境（如果有）
.\venv\Scripts\Activate.ps1  # 如果虚拟环境使用 Python 3.13
python main.py
```

### 方案 2: 创建虚拟环境（最佳实践）

```powershell
# 使用 Python 3.13 创建虚拟环境
py -3.13 -m venv venv

# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 安装依赖
pip install -r requirements.txt

# 运行脚本
python main.py
```

### 方案 3: 为 Python 3.14 安装依赖（不推荐）

虽然不推荐，但如果必须使用 Python 3.14：

```powershell
# 使用 Python 3.14 安装依赖
C:/Python314/python.exe -m pip install -r requirements.txt

# 运行
C:/Python314/python.exe main.py
```

⚠️ **注意**：Python 3.14 可能不被所有包支持，可能遇到兼容性问题。

## 快速修复命令

### 立即使用 Python 3.13 运行：

```powershell
# 切换到项目目录
cd C:\Users\DAI\Desktop\OpenManus-main

# 使用 Python 3.13 运行
py -3.13 main.py
```

### 如果需要指定提示参数：

```powershell
py -3.13 main.py --prompt "你的提示内容"
```

## 设置默认 Python 版本（可选）

### 方法 1: 修改 PATH 环境变量
将 Python 3.13 的路径放在 Python 3.14 之前

### 方法 2: 使用 py.ini 配置文件
在用户目录创建 `py.ini` 文件，设置默认版本

### 方法 3: 创建项目脚本
创建一个 `run.bat` 或 `run.ps1` 文件，固定使用 Python 3.13

## 推荐的运行方式

**创建 `run.ps1` 脚本：**

```powershell
# run.ps1
py -3.13 main.py $args
```

然后运行：
```powershell
.\run.ps1 --prompt "你的提示"
```

或者直接：
```powershell
.\run.ps1
```

## 验证修复

修复后，验证：

```powershell
# 检查 Python 版本
py -3.13 --version

# 检查 pydantic 是否可用
py -3.13 -c "import pydantic; print(pydantic.__version__)"

# 测试运行
py -3.13 main.py
```


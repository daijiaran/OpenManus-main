@echo off
REM OpenManus GUI 启动脚本 (Windows)

echo 🚀 启动 OpenManus Desktop GUI...

REM 检查 Python
python --version
if errorlevel 1 (
    echo ❌ Python 未安装或未添加到 PATH
    pause
    exit /b 1
)

REM 检查依赖
python -c "import PyQt6" 2>nul
if errorlevel 1 (
    echo ❌ PyQt6 未安装
    echo 正在安装 GUI 依赖...
    pip install -r requirements-gui.txt
)

REM 启动 GUI
echo ✅ 启动应用...
python gui_main.py

echo 👋 应用已关闭
pause

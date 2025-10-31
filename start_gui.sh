#!/bin/bash
# OpenManus GUI 启动脚本

echo "🚀 启动 OpenManus Desktop GUI..."

# 检查 Python 版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python 版本: $python_version"

# 检查依赖
if ! python3 -c "import PyQt6" 2>/dev/null; then
    echo "❌ PyQt6 未安装"
    echo "正在安装 GUI 依赖..."
    pip3 install -r requirements-gui.txt
fi

# 启动 GUI
echo "✅ 启动应用..."
python3 gui_main.py

echo "👋 应用已关闭"

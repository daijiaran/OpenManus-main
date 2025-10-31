#!/usr/bin/env python3
"""
GUI 功能测试脚本
测试 GUI 组件是否能正常导入和初始化
"""

import sys
import traceback


def test_imports():
    """测试依赖导入"""
    print("=" * 60)
    print("测试 1: 检查依赖导入")
    print("=" * 60)
    
    try:
        print("✓ 导入 sys, asyncio...")
        import asyncio
        
        print("✓ 导入 PyQt6...")
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import Qt
        
        print("✓ 导入 qasync...")
        import qasync
        from qasync import QEventLoop
        
        print("✓ 导入 OpenManus 组件...")
        from app.agent.manus import Manus
        from app.schema import AgentState, Memory
        from app.logger import logger
        
        print("\n✅ 所有依赖导入成功!\n")
        return True
        
    except ImportError as e:
        print(f"\n❌ 导入失败: {e}")
        print(f"\n详细错误:\n{traceback.format_exc()}")
        return False


def test_gui_structure():
    """测试 GUI 结构"""
    print("=" * 60)
    print("测试 2: 检查 GUI 文件结构")
    print("=" * 60)
    
    import os
    
    files_to_check = [
        "gui_main.py",
        "gui_enhanced.py",
        "requirements-gui.txt",
        "start_gui.sh",
        "start_gui.bat",
        "GUI_README.md",
        "GUI_DESIGN.md"
    ]
    
    all_exist = True
    for file in files_to_check:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} (缺失)")
            all_exist = False
    
    if all_exist:
        print("\n✅ 所有 GUI 文件存在!\n")
    else:
        print("\n⚠️ 部分文件缺失\n")
    
    return all_exist


def test_syntax():
    """测试 Python 语法"""
    print("=" * 60)
    print("测试 3: 检查 Python 语法")
    print("=" * 60)
    
    import py_compile
    
    files_to_check = ["gui_main.py", "gui_enhanced.py"]
    
    all_valid = True
    for file in files_to_check:
        try:
            py_compile.compile(file, doraise=True)
            print(f"✓ {file} 语法正确")
        except py_compile.PyCompileError as e:
            print(f"✗ {file} 语法错误: {e}")
            all_valid = False
    
    if all_valid:
        print("\n✅ 所有文件语法正确!\n")
    else:
        print("\n❌ 存在语法错误\n")
    
    return all_valid


def test_config():
    """测试配置文件"""
    print("=" * 60)
    print("测试 4: 检查配置文件")
    print("=" * 60)
    
    import os
    
    config_path = "config/config.toml"
    example_path = "config/config.example.toml"
    
    if os.path.exists(config_path):
        print(f"✓ {config_path} 存在")
        config_ok = True
    else:
        print(f"⚠️ {config_path} 不存在")
        if os.path.exists(example_path):
            print(f"  提示: 可以从 {example_path} 复制")
        config_ok = False
    
    if config_ok:
        print("\n✅ 配置文件检查通过!\n")
    else:
        print("\n⚠️ 需要配置文件\n")
    
    return config_ok


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("OpenManus Desktop GUI - 功能测试")
    print("=" * 60 + "\n")
    
    results = {
        "依赖导入": test_imports(),
        "文件结构": test_gui_structure(),
        "语法检查": test_syntax(),
        "配置文件": test_config()
    }
    
    print("=" * 60)
    print("测试总结")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有测试通过! GUI 已准备就绪。")
        print("\n启动方式:")
        print("  Linux/macOS: ./start_gui.sh")
        print("  Windows: start_gui.bat")
        print("  或直接运行: python3 gui_enhanced.py")
    else:
        print("⚠️ 部分测试未通过，请检查上述错误。")
        print("\n常见问题:")
        print("  1. 依赖未安装: pip install -r requirements-gui.txt")
        print("  2. 配置缺失: cp config/config.example.toml config/config.toml")
    print("=" * 60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

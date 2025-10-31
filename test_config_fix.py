"""
测试配置和 Daytona 修复的简单测试脚本
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_config_loading():
    """测试配置加载是否正常"""
    print("=" * 60)
    print("测试 1: 配置加载")
    print("=" * 60)

    try:
        from app.config import config
        print("[OK] 配置加载成功")

        # 测试 Daytona 配置
        daytona_config = config.daytona
        print(f"[OK] Daytona API key 类型: {type(daytona_config.daytona_api_key)}")
        print(f"[OK] Daytona API key 值: '{daytona_config.daytona_api_key}'")
        print(f"[OK] Daytona API key 是否为空: {not daytona_config.daytona_api_key}")

        # 验证 API key 是可选的
        assert daytona_config.daytona_api_key is not None, "API key 应该存在（即使是空字符串）"
        print("[OK] API key 字段存在（可选字段验证通过）")

        return True
    except Exception as e:
        print(f"[FAIL] 配置加载失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_daytona_import():
    """测试 Daytona 模块导入是否正常（不要求 API key）"""
    print("\n" + "=" * 60)
    print("测试 2: Daytona 模块导入（无 API key）")
    print("=" * 60)

    try:
        # 尝试导入 Daytona 相关模块
        from app.daytona.sandbox import daytona, daytona_settings
        print("[OK] Daytona 模块导入成功")

        # 验证 daytona 实例
        if daytona is None:
            print("[OK] daytona 实例为 None（预期的，因为没有 API key）")
        else:
            print("[WARN]  daytona 实例不为 None（如果配置了 API key，这是正常的）")

        # 验证设置
        print(f"[OK] daytona_settings 加载成功")
        print(f"   服务器 URL: {daytona_settings.daytona_server_url}")
        print(f"   目标区域: {daytona_settings.daytona_target}")

        return True
    except Exception as e:
        print(f"[FAIL] Daytona 模块导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_daytona_tool_base_import():
    """测试 Daytona tool_base 模块导入"""
    print("\n" + "=" * 60)
    print("测试 3: Daytona tool_base 模块导入")
    print("=" * 60)

    try:
        from app.daytona.tool_base import SandboxToolsBase, daytona
        print("[OK] tool_base 模块导入成功")

        if daytona is None:
            print("[OK] daytona 实例为 None（预期的，因为没有 API key）")
        else:
            print("[WARN]  daytona 实例不为 None")

        print("[OK] SandboxToolsBase 类可以正常导入")
        return True
    except Exception as e:
        print(f"[FAIL] tool_base 模块导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_main_import():
    """测试主程序模块导入"""
    print("\n" + "=" * 60)
    print("测试 4: 主程序模块导入")
    print("=" * 60)

    try:
        # 尝试导入主模块依赖
        from app.agent.manus import Manus
        print("[OK] Manus agent 导入成功")

        from app.agent.browser import BrowserAgent
        print("[OK] BrowserAgent 导入成功")

        from app.tool.sandbox.sb_browser_tool import SandboxBrowserTool
        print("[OK] SandboxBrowserTool 导入成功")

        return True
    except Exception as theoretical:
        print(f"[FAIL] 主程序模块导入失败: {theoretical}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """运行所有测试"""
    print("\n开始测试配置和 Daytona 修复\n")

    results = []

    results.append(("配置加载", test_config_loading()))
    results.append(("Daytona 模块导入", test_daytona_import()))
    results.append(("Daytona tool_base 导入", test_daytona_tool_base_import()))
    results.append(("主程序模块导入", test_main_import()))

    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "[OK] 通过" if result else "[FAIL] 失败"
        print(f"{status} - {name}")

    print(f"\n总计: {passed}/{total} 个测试通过")

    if passed == total:
        print("\n[成功] 所有测试通过！修复成功！")
        return 0
    else:
        print(f"\n[警告] 有 {total - passed} 个测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())


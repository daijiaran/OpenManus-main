#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试豆包 API 连接"""
import asyncio
import io
import sys
from pathlib import Path

# 设置输出编码（Windows 兼容）
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

try:
    from app.config import Config
    from app.llm import LLM

    async def test_doubao():
        print("=" * 50)
        print("测试豆包 API 配置和连接")
        print("=" * 50)

        # 加载配置
        config = Config()
        llm_config = config.llm["default"]  # 获取默认 LLM 配置

        print(f"\n[配置信息]")
        print(f"API 类型: {llm_config.api_type}")
        print(f"模型: {llm_config.model}")
        print(f"API 地址: {llm_config.base_url}")
        api_key_preview = (
            llm_config.api_key[:20]
            if len(llm_config.api_key) > 20
            else llm_config.api_key
        )
        print(f"API Key: {api_key_preview}...")  # 只显示前20个字符

        # 测试 LLM 初始化
        print(f"\n[初始化测试]")
        try:
            llm = LLM()
            print(f"[OK] LLM 客户端初始化成功")
            print(f"  - Model: {llm.model}")
            print(f"  - Base URL: {llm.base_url}")
            print(f"  - API Type: {llm.api_type}")
        except Exception as e:
            print(f"[ERROR] LLM 初始化失败: {e}")
            import traceback

            traceback.print_exc()
            return

        # 测试 API 调用
        print(f"\n[API 调用测试]")
        try:
            test_messages = [
                {"role": "user", "content": "你好，请用一句话介绍你自己。"}
            ]

            print(f"发送测试消息: {test_messages[0]['content']}")
            response = await llm.ask_tool(
                messages=test_messages, tools=[], tool_choice="auto"
            )

            if response and response.content:
                print(f"[OK] API 调用成功！")
                print(f"  响应: {response.content[:200]}...")
            else:
                print(f"[WARNING] API 返回了空响应")

        except Exception as e:
            print(f"[ERROR] API 调用失败: {e}")
            import traceback

            traceback.print_exc()

        print(f"\n{'=' * 50}")
        print("测试完成！")
        print("=" * 50)

    if __name__ == "__main__":
        asyncio.run(test_doubao())

except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保在项目根目录运行此脚本")
except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()

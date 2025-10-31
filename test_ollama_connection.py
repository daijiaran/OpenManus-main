#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试 Ollama 连接和配置"""
import sys
import asyncio
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

try:
    from app.config import Config

    async def test_config():
        print("=" * 50)
        print("测试 Ollama 配置和连接")
        print("=" * 50)

        # 加载配置
        config = Config()
        llm_config = config.get_llm_config()

        print(f"\n[配置信息]")
        print(f"API 类型: {llm_config.get('api_type')}")
        print(f"模型: {llm_config.get('model')}")
        print(f"API 地址: {llm_config.get('base_url')}")

        # 测试连接
        print(f"\n[连接测试]")
        import httpx

        try:
            base_url = llm_config.get('base_url', '').replace('/v1', '')
            async with httpx.AsyncClient(timeout=10.0) as client:
                # 检查 Ollama 服务是否运行
                response = await client.get(f"{base_url}/api/tags")
                if response.status_code == 200:
                    models = response.json().get('models', [])
                    print(f"✓ Ollama 服务运行正常")
                    print(f"✓ 已安装的模型数量: {len(models)}")

                    model_name = llm_config.get('model')
                    model_found = any(m.get('name', '').startswith(model_name) for m in models)

                    if model_found:
                        print(f"✓ 找到配置的模型: {model_name}")
                    else:
                        print(f"⚠ 未找到模型: {model_name}")
                        print(f"  可用模型: {[m.get('name') for m in models[:5]]}")

                    # 测试模型调用
                    print(f"\n[模型测试]")
                    test_prompt = "你好，请用一句话介绍你自己。"
                    print(f"测试提示: {test_prompt}")

                    chat_url = f"{base_url}/api/chat"
                    test_data = {
                        "model": model_name,
                        "messages": [
                            {"role": "user", "content": test_prompt}
                        ],
                        "stream": False
                    }

                    response = await client.post(chat_url, json=test_data, timeout=30.0)
                    if response.status_code == 200:
                        result = response.json()
                        answer = result.get('message', {}).get('content', '')
                        print(f"✓ 模型响应成功:")
                        print(f"  {answer[:200]}...")
                    else:
                        print(f"✗ 模型调用失败: {response.status_code}")
                        print(f"  错误信息: {response.text}")
                else:
                    print(f"✗ Ollama 服务连接失败: {response.status_code}")

        except httpx.ConnectError:
            print(f"✗ 无法连接到 Ollama 服务")
            print(f"  请确保 Ollama 正在运行")
            print(f"  可以尝试运行: ollama serve")
        except Exception as e:
            print(f"✗ 连接测试出错: {e}")

        print(f"\n{'=' * 50}")
        print("测试完成！如果看到 ✓ 标记，说明配置正确。")
        print("现在可以运行: python main.py")
        print("=" * 50)

    if __name__ == "__main__":
        asyncio.run(test_config())

except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保在项目根目录运行此脚本")
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()


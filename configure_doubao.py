#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""豆包 API 配置助手"""
import io
import os
import sys
from pathlib import Path

# 设置输出编码（Windows 兼容）
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def configure_doubao():
    print("=" * 60)
    print("豆包 API 配置助手")
    print("=" * 60)
    print()
    print("根据豆包文档，你需要配置以下信息：")
    print("1. 推理接入点 ID（Model ID 或 Endpoint ID）")
    print("2. API Key")
    print()
    print("提示：")
    print("- 如果使用 Model ID：格式类似 doubao-lite-32k")
    print("- 如果使用 Endpoint ID：格式类似 doubao-seed-1-6-251015 或 ep-xxxxx")
    print("- API Key 可以从环境变量 ARK_API_KEY 读取，或直接输入")
    print()
    print("-" * 60)

    # 读取当前配置（如果存在）
    config_path = Path("config/config.toml")
    current_model = ""
    current_api_key = ""

    if config_path.exists():
        try:
            import tomllib

            with config_path.open("rb") as f:
                data = tomllib.load(f)
                if "llm" in data:
                    current_model = data["llm"].get("model", "")
                    current_api_key = data["llm"].get("api_key", "")
        except Exception:
            pass

    # 1. 获取 Model ID / Endpoint ID
    print("\n[1/2] 配置推理接入点 ID")
    if current_model and current_model not in [
        "doubao-seed-1-6-251015",
        "YOUR_MODEL_ID",
    ]:
        print(f"当前配置: {current_model}")
        use_current = input("是否使用当前配置？(Y/n): ").strip().lower()
        if use_current != "n":
            model_id = current_model
        else:
            model_id = input(
                "请输入你的推理接入点 ID (Model ID 或 Endpoint ID): "
            ).strip()
    else:
        print("提示：在豆包控制台查看你的 Model ID 或 Endpoint ID")
        model_id = input("请输入推理接入点 ID: ").strip()

    if not model_id:
        print("错误：推理接入点 ID 不能为空！")
        return

    # 2. 获取 API Key
    print("\n[2/2] 配置 API Key")

    # 检查环境变量
    env_api_key = os.environ.get("ARK_API_KEY")
    if env_api_key:
        print(f"检测到环境变量 ARK_API_KEY")
        use_env = input("是否使用环境变量中的 API Key？(Y/n): ").strip().lower()
        if use_env != "n":
            api_key = "YOUR_ARK_API_KEY"  # 使用占位符，代码会从环境变量读取
            print("✓ 将使用环境变量 ARK_API_KEY")
        else:
            api_key = input("请输入 API Key: ").strip()
    else:
        if current_api_key and current_api_key not in [
            "YOUR_ARK_API_KEY",
            "YOUR_API_KEY",
            "",
        ]:
            print(f"当前配置: {current_api_key[:20]}...")
            use_current = input("是否使用当前配置？(Y/n): ").strip().lower()
            if use_current != "n":
                api_key = current_api_key
            else:
                print("提示：可以直接输入 API Key，或稍后设置环境变量")
                print("如果设置环境变量，请输入: YOUR_ARK_API_KEY")
                api_key = input(
                    "请输入 API Key (或输入 YOUR_ARK_API_KEY 使用环境变量): "
                ).strip()
        else:
            print("提示：可以直接输入 API Key，或稍后设置环境变量 ARK_API_KEY")
            print("如果设置环境变量，请输入: YOUR_ARK_API_KEY")
            api_key = input(
                "请输入 API Key (或输入 YOUR_ARK_API_KEY 使用环境变量): "
            ).strip()

    if not api_key:
        print("警告：API Key 为空，将使用占位符（需要设置环境变量）")
        api_key = "YOUR_ARK_API_KEY"

    # 3. 确认配置
    print("\n" + "=" * 60)
    print("配置预览：")
    print("=" * 60)
    print(f"推理接入点 ID: {model_id}")
    if api_key == "YOUR_ARK_API_KEY":
        print(f"API Key: {api_key} (将从环境变量读取)")
    else:
        print(f"API Key: {api_key[:20]}...")
    print("=" * 60)

    confirm = input("\n确认保存配置？(Y/n): ").strip().lower()
    if confirm == "n":
        print("已取消配置")
        return

    # 4. 更新配置文件
    try:
        # 读取现有配置
        config_content = (
            config_path.read_text(encoding="utf-8") if config_path.exists() else ""
        )

        # 构建新的 LLM 配置部分
        new_llm_section = f"""# 全局 LLM 配置 - 使用豆包（Doubao）API
# 配置时间: {os.popen('date /t' if sys.platform == 'win32' else 'date').read().strip()}
[llm]
api_type = "doubao"                                                      # API 类型：doubao（豆包）
 Score = "{model_id}"                                        # 推理接入点 ID（Model ID 或 Endpoint ID）
base_url = "https://ark.cn-beijing.volces.com/api/v3"                   # 方舟API基础端点（不包含 /chat/completions）
api_key = "{api_key}"                                            # API密钥（YOUR_ARK_API_KEY 表示从环境变量读取）
max_tokens = 8192                                                        # 响应最大token数
temperature = 0.0                                                        # 控制随机性（0-1之间）

"""

        # 如果配置文件存在，替换 [llm] 部分
        if config_path.exists() and "[llm]" in config_content:
            lines = config_content.split("\n")
            new_lines = []
            skip_until_blank = False

            for i, line in enumerate(lines):
                if line.strip().startswith("[llm]"):
                    # 找到 [llm] 开始位置
                    new_lines.append(new_llm_section.rstrip())
                    skip_until_blank = True
                    continue
                elif skip_until_blank:
                    # 跳过直到下一个 [ 开头的节或空行
                    if line.strip().startswith("[") or (
                        line.strip() == ""
                        and i < len(lines) - 1
                        and lines[i + 1].strip().startswith("[")
                    ):
                        skip_until_blank = False
                        new_lines.append(line)
                    continue
                else:
                    new_lines.append(line)

            config_content = "\n".join(new_lines)
        else:
            # 如果不存在或没有 [llm] 部分，追加
            if not config_content.endswith("\n"):
                config_content += "\n"
            config_content += new_llm_section

        # 写入文件
        config_path.write_text(config_content, encoding="utf-8")

        print("\n✓ 配置已保存到 config/config.toml")
        print("\n下一步：")
        print("1. 如果使用环境变量，请设置: $env:ARK_API_KEY = '你的密钥'")
        print("2. 运行测试: python test_doubao_connection.py")
        print("3. 或直接运行: python main.py")

    except Exception as e:
        print(f"\n✗ 保存配置失败: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    try:
        configure_doubao()
    except KeyboardInterrupt:
        print("\n\n已取消配置")
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback

        traceback.print_exc()

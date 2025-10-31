# 豆包 API 配置说明

## 📋 当前配置状态

配置文件：`config/config.toml`

**当前需要配置的内容**：

```toml
[llm]
api_type = "doubao"
model = "doubao-seed-1-6-251015"          # ⚠️ 需要替换为你的实际ID
api_key = "YOUR_ARK_API_KEY"              # ⚠️ 需要配置API密钥
base_url = "https://ark.cn-beijing.volces.com/api/v3"
max_tokens = 8192
temperature = 0.0
```

## 🔧 配置步骤

### 步骤 1：获取推理接入点 ID

1. 登录[火山引擎豆包控制台](https://console.volcengine.com/)
2. 进入"推理接入点"页面
3. 找到你的接入点，复制 **Endpoint ID**
   - 格式可能类似：`doubao-seed-1-6-251015` 或 `ep-xxxxx`
4 can 或者在"模型列表"中查看 **Model ID**
   - 格式可能类似：`doubao-lite-32k`、`doubao-pro-32k`

### 步骤 2：获取 API Key

1. 在豆包控制台找到"API Key 管理"
2. 创建或查看现有的 API Key
3. 复制 API Key

### 步骤 3：更新配置文件

打开 `config/config.toml`，修改：

```toml
model = "你的实际推理接入点ID"      # 替换这里
api_key = "你的实际API密钥"          # 替换这里
```

**或者使用环境变量（推荐）**：

1. 设置环境变量：
   ```powershell
   # Windows PowerShell
   $env:ARK_API_KEY = "你的API密钥"
   ```

2. 配置文件中保持：
   ```toml
   api_key = "YOUR_ARK_API_KEY"  # 会自动从环境变量读取
   ```

## ✅ 验证配置

运行测试脚本：

```bash
python test_doubao_connection.py
```

如果看到 `[OK] API 调用成功！`，说明配置正确！

## 🚀 开始使用

配置完成后，直接运行：

```bash
python main.py
```

## 📚 更多说明

- 详细配置说明：查看 `豆包接入点说明.md`
- 快速配置指南：查看 `快速配置指南.md`
- 常见问题：查看 `配置说明.md`

## ❓ 需要帮助？

如果你提供：
- 你的推理接入点 ID
- 你的 API Key（或确认使用环境变量）

我可以直接帮你更新配置文件！


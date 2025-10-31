# Ollama 免费模型配置指南

## 配置文件已创建

已为您创建了 `config/config.toml` 文件，使用 **Ollama** 作为免费本地模型服务。

## 使用步骤

### 1. 安装 Ollama

访问 https://ollama.com/ 下载并安装 Ollama（支持 Windows、Mac、Linux）

### 2. 启动 Ollama 服务

安装后，Ollama 服务会自动启动，默认运行在 `http://localhost:11434`

### 3. 下载模型

在终端中运行以下命令下载模型：

```bash
# 下载基础语言模型（推荐）
ollama pull llama3.2

# 如果需要视觉功能，下载视觉模型
ollama pull llama3.2-vision
```

### 4. 验证配置

运行以下命令验证 Ollama 是否正常工作：

```bash
ollama run llama3.2
```

如果能看到模型响应，说明配置成功！

### 5. 运行项目

现在您可以直接运行项目了：

```bash
python main.py
```

## 其他可用模型

Ollama 支持多种免费模型，您可以根据需要下载：

```bash
# 中文友好模型
ollama pull qwen2.5
ollama pull qwen2.5-vision

# 其他模型
ollama pull mistral
ollama pull codellama
ollama pull phi3
```

下载后，在 `config/config.toml` 中修改 `model` 字段即可切换模型。

## 注意事项

1. **首次使用**：下载模型需要一些时间和网络带宽
2. **内存要求**：确保有足够的 RAM（通常需要 4GB+）
3. **本地运行**：所有数据都在本地处理，保护隐私
4. **无需 API Key**：完全免费，无需注册或付费

## 切换到其他服务

如果需要使用在线 API 服务（如 Claude、GPT 等），可以：
1. 打开 `config/config.toml`
2. 注释掉当前的 `[llm]` 配置
3. 取消注释并配置相应的服务（如 Azure OpenAI、Anthropic 等）
4. 填入相应的 API Key

## 问题排查

### Ollama 服务未启动
```bash
# Windows: 检查服务是否运行
# Mac/Linux: 启动服务
ollama serve
```

### 连接错误
确保 Ollama 服务运行在 `http://localhost:11434`，可以在浏览器访问该地址验证。

### 模型未找到
运行 `ollama pull <model_name>` 下载相应的模型。


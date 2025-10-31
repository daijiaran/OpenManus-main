# OpenManus Desktop GUI - 快速启动指南

## 5 分钟快速上手 🚀

### 前置条件
- ✅ Python 3.12+
- ✅ 有效的 OpenAI API Key（或兼容的 LLM API）

### 步骤 1: 安装依赖（2 分钟）

```bash
# 克隆项目（如果还没有）
git clone https://github.com/FoundationAgents/OpenManus.git
cd OpenManus

# 安装所有依赖（包括 GUI）
pip install -r requirements-gui.txt
```

### 步骤 2: 配置 API（1 分钟）

```bash
# 复制配置文件
cp config/config.example.toml config/config.toml

# 编辑配置文件，填入您的 API Key
# 使用您喜欢的编辑器打开 config/config.toml
# 修改 api_key = "sk-..." 为您的实际 API Key
```

**配置示例**:
```toml
[llm]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-your-actual-api-key-here"  # ← 修改这里
max_tokens = 4096
temperature = 0.0
```

### 步骤 3: 启动 GUI（1 分钟）

#### Linux/macOS
```bash
python3 gui_enhanced.py
```

#### Windows
```batch
python gui_enhanced.py
```

### 步骤 4: 开始使用（1 分钟）

1. **等待初始化**: 应用启动后，等待状态指示器变为 🟢 绿色
2. **输入任务**: 在输入框中输入您的任务，例如：
   - "帮我写一个 Python 脚本，计算斐波那契数列"
   - "分析一下当前的 AI 发展趋势"
   - "创建一个简单的待办事项列表网页"
3. **发送**: 点击「发送」按钮或按 Enter 键
4. **查看结果**: 在对话区域查看 Agent 的响应

## 界面预览

```
┌─────────────────────────────────────────────────────┐
│ 🤖 OpenManus AI Agent              🟢 就绪          │
├─────────────────────────────────────────────────────┤
│ [💬 对话] [📋 日志]                                  │
│                                                     │
│ ┌─────────────────────────────────────────────────┐│
│ │ 👤 用户 [14:23:45]                              ││
│ │ 帮我写一个 Python 脚本                           ││
│ │                                                 ││
│ │ 🤖 Manus [14:23:50]                             ││
│ │ 好的，我来帮你创建...                           ││
│ └─────────────────────────────────────────────────┘│
│                                                     │
│ ┌─────────────────────────────────────────────────┐│
│ │ 输入您的任务指令...                    [发送 ▶] ││
│ └─────────────────────────────────────────────────┘│
│ ☐ 保持对话记忆  [清空对话] [停止任务]              │
│                                                     │
│ 状态: 就绪 | 任务计数: 1 | 当前步骤: 0              │
└─────────────────────────────────────────────────────┘
```

## 常用功能

### 💬 对话模式
- **单次对话**: 不勾选「保持对话记忆」，每次都是新对话
- **连续对话**: 勾选「保持对话记忆」，保留上下文

### 📋 日志查看
切换到「日志」标签页，查看详细的执行过程

### 💾 导出功能
- **导出对话**: 菜单 → 文件 → 导出对话记录
- **导出日志**: 菜单 → 文件 → 导出日志

## 示例任务

试试这些任务来体验 OpenManus 的能力：

### 1. 代码生成
```
创建一个 Python 函数，用于计算两个日期之间的天数差
```

### 2. 数据分析
```
帮我分析一下 [数据集链接]，并生成可视化图表
```

### 3. 文本处理
```
总结以下文章的主要内容：[文章内容或链接]
```

### 4. 创意写作
```
写一个关于 AI 助手的短故事，500 字左右
```

### 5. 技术问答
```
解释一下什么是 Transformer 架构，以及它在 NLP 中的应用
```

## 故障排除

### ❌ 启动失败
```bash
# 检查依赖
python3 test_gui.py

# 重新安装依赖
pip install -r requirements-gui.txt
```

### ❌ Agent 初始化失败
- 检查 `config/config.toml` 中的 API Key 是否正确
- 确认网络连接正常
- 查看日志标签页的详细错误信息

### ❌ 界面显示异常
- 尝试调整窗口大小
- 重启应用

## 进阶使用

详细文档请参考：
- [GUI_README.md](GUI_README.md) - 完整使用文档
- [GUI_INSTALL.md](GUI_INSTALL.md) - 详细安装指南
- [GUI_DESIGN.md](GUI_DESIGN.md) - 设计文档

## 版本选择

- **gui_enhanced.py** (推荐): 功能完整，界面美观
- **gui_main.py** (基础版): 轻量简洁，快速启动

## 快捷键

- `Enter`: 发送消息
- `Ctrl+Q`: 退出应用（Linux/macOS）

## 获取帮助

- 📖 查看帮助菜单中的「使用文档」
- 🐛 遇到问题？提交 Issue: https://github.com/FoundationAgents/OpenManus/issues
- 💬 加入社区讨论

---

**开始您的 AI Agent 之旅！** 🎉

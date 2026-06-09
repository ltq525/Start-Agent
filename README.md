# StartAgent

StartAgent 是一个灵活、可扩展的多智能体框架，基于 OpenAI 兼容接口构建，目标是提供简洁的 Agent 开发、工具调用、记忆管理、协议适配、评测和强化学习训练能力。

## 功能特性

- 多种 Agent 范式：`SimpleAgent`、`ReActAgent`、`ReflectionAgent`、`PlanAndSolveAgent`、`ToolAwareSimpleAgent`、`FunctionCallAgent`
- 统一 LLM 接口：支持 OpenAI、DeepSeek、通义千问、ModelScope、Kimi、智谱、Ollama、vLLM、本地和自定义 OpenAI 兼容服务
- 工具系统：支持工具注册、函数工具、工具链、异步执行以及内置计算器、搜索、记忆、RAG、终端、评测和协议工具
- 记忆与 RAG：包含工作记忆、情节记忆、语义记忆、感知记忆、SQLite 文档存储、Qdrant 向量存储和 Neo4j 图存储扩展
- 协议支持：包含 MCP、A2A、ANP 等协议相关实现
- 评测与数据生成：支持 BFCL、GAIA、LLM Judge、Win Rate 等评测流程
- 强化学习模块：包含 SFT、GRPO、PPO 训练包装、数据集处理和奖励函数工具

## 项目结构

```text
start_agent/
  agents/        Agent 实现
  core/          LLM、配置、消息和异常等核心组件
  tools/         工具基类、注册表、内置工具和工具执行器
  memory/        记忆系统、RAG 管线和存储后端
  protocols/     MCP、A2A、ANP 协议适配
  evaluation/    BFCL、GAIA、数据生成和自动评测
  rl/            强化学习训练、数据集和奖励函数
  context/       上下文构建工具
  utils/         日志、序列化和辅助函数
tests/           基础烟测
```

## 环境要求

- Python 3.10+
- 推荐使用虚拟环境

项目当前没有提供 `pyproject.toml` 或 `requirements.txt`，可以先按需安装基础依赖：

```bash
python -m venv .venv
source .venv/bin/activate
pip install openai pydantic requests pytest
```

如果使用记忆、搜索、评测、协议或 RL 模块，可能还需要安装以下可选依赖：

```bash
pip install numpy python-dotenv qdrant-client neo4j tiktoken fastmcp
pip install markdownify ddgs tavily-python google-search-results
pip install huggingface_hub datasets transformers trl
```

## 配置

StartAgent 会优先读取构造参数，其次读取环境变量。常用变量如下：

```bash
export LLM_API_KEY="your-api-key"
export LLM_BASE_URL="https://api.openai.com/v1"
export LLM_MODEL_ID="gpt-3.5-turbo"
export LLM_TIMEOUT="60"
```

也可以使用特定服务商变量：

```bash
export OPENAI_API_KEY="..."
export DEEPSEEK_API_KEY="..."
export DASHSCOPE_API_KEY="..."
export MODELSCOPE_API_KEY="..."
export KIMI_API_KEY="..."
export ZHIPU_API_KEY="..."
export OLLAMA_HOST="http://localhost:11434/v1"
```

搜索工具可选变量：

```bash
export TAVILY_API_KEY="..."
export SERPAPI_API_KEY="..."
export PERPLEXITY_API_KEY="..."
```

请不要将 `.env` 或任何 API Key 提交到公开仓库。

## 快速开始

### 运行基础工具

计算器工具不依赖外部服务：

```python
from start_agent.tools.builtin.calculator import calculate

print(calculate("sqrt(16) + 2 * 3"))
```

### 调用 LLM

```python
from start_agent import StartAgentLLM, SimpleAgent

llm = StartAgentLLM(
    provider="openai",
    model="gpt-3.5-turbo",
)

agent = SimpleAgent(
    name="assistant",
    llm=llm,
    system_prompt="你是一个简洁、可靠的 AI 助手。",
)

print(agent.run("用一句话介绍 StartAgent。"))
```

### 注册函数工具

```python
from start_agent import StartAgentLLM, ReActAgent, ToolRegistry

registry = ToolRegistry()
registry.register_function(
    name="echo",
    description="原样返回输入内容",
    func=lambda text: text,
)

llm = StartAgentLLM(provider="openai")
agent = ReActAgent(name="react-agent", llm=llm, tool_registry=registry)

print(agent.run("请调用 echo 工具返回 hello"))
```

## 测试

```bash
pytest
```

当前测试包含包导出、旧包名不可导入以及计算器工具烟测。

## 开发说明

- `StartAgentLLM` 封装任何 OpenAI 兼容的 Chat Completions 服务。
- `ToolRegistry` 负责注册、查找和执行工具。
- 内置搜索工具支持 Tavily、SerpApi、DuckDuckGo、SearXNG、Perplexity 等后端，其中部分后端需要额外依赖和 API Key。
- 记忆和 RAG 模块可能使用 SQLite、Qdrant、Neo4j、NumPy、嵌入模型等组件，请按实际功能安装依赖。
- RL 模块依赖 Hugging Face、Transformers 和 TRL 生态，建议单独隔离环境。

## 声明

本项目按现状提供，示例代码和工具调用结果仅用于学习、研究和工程实验。使用第三方模型、搜索服务、向量数据库或评测数据集时，请遵守对应服务商、数据集和开源组件的许可协议、使用条款及隐私要求。

## 许可证

本项目采用 MIT License 开源。详见 [LICENSE](LICENSE)。


# StartAgent Environment Guide

本文档用于指导 StartAgent 的本地环境、可选依赖和环境变量配置。StartAgent 的模块较多，建议按使用场景分层安装依赖，而不是一次性安装所有重型组件。

## 快速路径

| 场景 | 需要配置 |
| --- | --- |
| 只运行基础工具和 demo 测试 | Python、`openai`、`pydantic`、`requests`、`pytest` |
| 调用 LLM Agent | 基础依赖、LLM API Key、模型名、Base URL |
| 使用搜索工具 | 基础依赖、搜索后端依赖、搜索 API Key |
| 使用 Memory / RAG | 基础依赖、NumPy、Qdrant 或 SQLite、可选 Neo4j、Embedding 配置 |
| 使用 MCP / A2A / ANP | 协议相关 SDK，例如 `fastmcp`、`a2a-sdk` |
| 使用评测工具 | 评测数据、LLM 配置、可选搜索和文件系统工具 |
| 使用 Agentic RL | Hugging Face、Transformers、TRL、PyTorch、Accelerate、TensorBoard |

## Python 环境

推荐 Python 3.10+，并为项目创建独立虚拟环境：

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

基础依赖：

```bash
pip install openai pydantic requests pytest
```

## 可选依赖

### 记忆、RAG 和上下文构建

```bash
pip install numpy python-dotenv qdrant-client neo4j tiktoken
```

### 搜索工具

```bash
pip install markdownify ddgs tavily-python google-search-results
```

### 协议适配

```bash
pip install fastmcp
pip install a2a-sdk
```

ANP 当前是概念性实现，默认不要求额外依赖。

### Agentic RL

```bash
pip install huggingface_hub datasets transformers trl accelerate torch tensorboard
```

RL 训练会下载模型和数据集，建议使用独立环境，并优先用小模型、小样本验证流程。

## 环境变量文件

从示例文件复制本地配置：

```bash
cp .env.example .env
```

`.env` 会被 `.gitignore` 忽略，不应提交到仓库。`.env.example` 只保留变量名和占位符，用于说明需要配置哪些项目。

## LLM 配置

通用 OpenAI 兼容配置：

```bash
LLM_MODEL_ID="gpt-3.5-turbo"
LLM_API_KEY="your-llm-api-key"
LLM_BASE_URL="https://api.openai.com/v1"
LLM_PROVIDER="custom"
LLM_TIMEOUT="60"
```

也可以使用特定服务商变量：

```bash
OPENAI_API_KEY="your-openai-api-key"
DEEPSEEK_API_KEY="your-deepseek-api-key"
DASHSCOPE_API_KEY="your-dashscope-api-key"
MODELSCOPE_API_KEY="your-modelscope-api-key"
KIMI_API_KEY="your-kimi-api-key"
ZHIPU_API_KEY="your-zhipu-api-key"
OLLAMA_HOST="http://localhost:11434/v1"
```

`StartAgentLLM` 会优先使用构造参数，其次读取环境变量。

## 搜索配置

按需配置搜索服务：

```bash
SERPAPI_API_KEY="your-serpapi-api-key"
TAVILY_API_KEY="your-tavily-api-key"
PERPLEXITY_API_KEY="your-perplexity-api-key"
GOOGLE_SEARCH_HL="zh-cn"
GOOGLE_SEARCH_GL="cn"
```

如果没有配置 Tavily 或 SerpApi，搜索工具会尝试使用可用后端降级。

## 向量库和图数据库

### Qdrant

云服务：

```bash
QDRANT_URL="https://your-cluster-url.qdrant.io:6333"
QDRANT_API_KEY="your-qdrant-api-key"
```

本地服务：

```bash
QDRANT_URL="http://localhost:6333"
QDRANT_API_KEY=""
```

集合配置：

```bash
QDRANT_COLLECTION="start_agent_vectors"
QDRANT_VECTOR_SIZE="1024"
QDRANT_DISTANCE="cosine"
QDRANT_TIMEOUT="30"
```

### Neo4j

云服务：

```bash
NEO4J_URI="neo4j+s://your-instance.databases.neo4j.io"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="your-neo4j-password"
NEO4J_DATABASE="neo4j"
```

本地服务：

```bash
NEO4J_URI="bolt://localhost:7687"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="your-local-neo4j-password"
```

连接池配置：

```bash
NEO4J_MAX_CONNECTION_LIFETIME="3600"
NEO4J_MAX_CONNECTION_POOL_SIZE="50"
NEO4J_CONNECTION_TIMEOUT="60"
```

## Embedding 配置

```bash
EMBED_MODEL_TYPE="dashscope"
EMBED_MODEL_NAME="text-embedding-v3"
EMBED_API_KEY="your-embedding-api-key"
EMBED_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
EMBED_DIMENSION="1024"
EMBED_RES_LEVEL="1"
```

如果使用本地 embedding，请保持模型维度和 Qdrant 集合维度一致。

## GitHub 配置

部分自动化或工具可能需要 GitHub Token：

```bash
GITHUB_PERSONAL_ACCESS_TOKEN="your-github-personal-access-token"
```

只给 Token 授予当前任务所需的最小权限，并定期轮换。

## 验证环境

基础语法检查：

```bash
python -m compileall -q start_agent tests
```

运行 demo 测试：

```bash
pytest tests/test_start_agent_demo.py
```

如果提示 `No module named pytest`，先安装：

```bash
pip install pytest
```

验证计算器工具：

```bash
python -c "from start_agent.tools.builtin.calculator import calculate; print(calculate('2 + 3 * 4'))"
```

## 安全注意事项

- 不要提交 `.env`、私钥、Token、云数据库连接凭据。
- `.env.example` 中只能放占位符，不要放真实值。
- 如果真实密钥曾经进入 Git 历史或远端仓库，请立即轮换。
- 本地数据库、训练输出、模型 checkpoint 和日志文件建议保存在被忽略的目录中。

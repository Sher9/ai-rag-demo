# 知识库问答脚手架

基于 **Python FastAPI + LangChain** 和 **Vue3 + Vite + Element Plus** 的全栈 RAG 知识库问答系统，开箱即用。

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 🔄 **多模型兼容** | 一套代码在 DeepSeek / 豆包 / 通义千问之间无缝切换 |
| 📚 **文档自动向量化** | 上传 PDF、TXT、Markdown，自动解析分块入库 |
| 🧠 **RAG 知识库问答** | 自动检索相关片段，拼接上下文增强回答质量 |
| ⚡ **SSE 流式输出** | 打字机效果，实时展示 AI 生成过程 |
| 📎 **来源片段标注** | 回答附带参考文档和相似度分数 |
| 🪶 **内存向量库** | 默认 FAISS，零外部依赖开箱即跑 |
| 🔌 **按需扩展** | 可切换 Chroma / PGVector / Milvus 生产级向量库 |
| 🎨 **现代前端** | Vue3 + Element Plus + Markdown 高亮渲染 |

## 📁 项目结构

```
AI-RGAW/
├── README.md
│
├── ai-rag-py/                       # 🐍 后端 Python + LangChain（主推）
│   ├── requirements.txt                    #    Python 依赖
│   ├── main.py                             #    FastAPI 入口（uvicorn 启动）
│   ├── config.py                           #    多模型/向量库/分块配置
│   ├── models.py                           #    Pydantic 响应模型
│   ├── routers/
│   │   ├── documents.py                    #    POST /api/documents/upload
│   │   └── chat.py                         #    POST /api/chat/stream + /sources
│   ├── services/
│   │   ├── document_service.py             #    文档加载 → 分块 → 向量化入库
│   │   ├── vector_store_service.py         #    FAISS 向量库 + 语义检索
│   │   └── chat_service.py                 #    RAG 流式对话 + 来源提取
│   └── utils/
│       └── prompt.py                       #    RAG Prompt 模板
│
└── ai-rag-ui/                       # 🎨 前端 Vue3 + Vite（共用）
    ├── package.json
    ├── vite.config.ts                      #    Vite 配置 + 后端代理
    └── src/
        ├── main.ts                         #    入口
        ├── api/index.ts                    #    API 封装
        ├── views/HomeView.vue              #    主页（侧边栏 + 聊天区）
        └── components/
            ├── ChatWindow.vue              #    聊天窗口（SSE 流式处理）
            ├── MessageItem.vue             #    消息气泡（Markdown 渲染）
            ├── DocumentUpload.vue          #    文档上传弹窗
            └── SourceCitation.vue          #    来源片段标注
```

## 🚀 快速开始

### 环境要求

- **Python 3.10+**
- **Node.js 18+**

### 1. 启动后端

```bash
cd ai-rag-py

# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 安装依赖
pip install -r requirements.txt

# 配置 API Key（选一个你有的模型）
# Windows PowerShell:
$env:DEEPSEEK_API_KEY="sk-xxxxxxxx"
# 或
$env:DOUBAO_API_KEY="xxxxxxxx"
# 或
$env:QWEN_API_KEY="sk-xxxxxxxx"

# Linux / macOS:
export DEEPSEEK_API_KEY="sk-xxxxxxxx"

# 启动（--reload 热重载）
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

后端运行在 **http://localhost:8080**，可访问 http://localhost:8080/docs 查看 Swagger 文档。

### 2. 启动前端

```bash
cd ai-rag-ui

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端运行在 **http://localhost:3000**，已自动代理 API 请求到后端 8080 端口。

### 3. 开始使用

1. 打开浏览器访问 http://localhost:3000
2. 点击左侧「上传文档」，选择 PDF / TXT / Markdown 文件
3. 等待文档处理完成（自动分块 + 向量化入库）
4. 在输入框提问，查看 AI 基于文档的回答和来源标注

## 🔄 模型切换

只需修改 `ai-rag-py/config.py` 中的一行：

```python
# 最后一行
config = AppConfig(active_model="deepseek")   # 改为 "doubao" 或 "qwen"
```

三套模型预设已内置：

| 模型 | base-url | chat-model |
|------|----------|------------|
| **DeepSeek** | `https://api.deepseek.com` | `deepseek-chat` |
| **豆包 (Doubao)** | `https://ark.cn-beijing.volces.com/api/v3` | 需配置 endpoint-id |
| **通义千问 (Qwen)** | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen-plus` |

> 所有模型均使用 OpenAI 兼容接口，只需对应的 API Key，前端和后端代码无需任何改动。

## ⚙️ 核心配置

`ai-rag-py/config.py`：

```python
@dataclass
class AppConfig:
    active_model: str = "deepseek"      # 当前模型

    chunk: ChunkConfig = field(default_factory=lambda: ChunkConfig(
        chunk_size=800,                 # 分块大小
        chunk_overlap=100,              # 重叠大小
    ))

    retrieval: RetrievalConfig = field(default_factory=lambda: RetrievalConfig(
        top_k=4,                        # 检索返回数
        similarity_threshold=0.7,       # 相似度阈值
    ))
```

## 📡 API 接口

| 方法 | 路径 | Content-Type | 说明 |
|------|------|-------------|------|
| `POST` | `/api/documents/upload` | `multipart/form-data` | 上传文档，自动向量化入库 |
| `POST` | `/api/chat/stream` | `text/event-stream` | SSE 流式问答 |
| `POST` | `/api/chat/sources` | `application/json` | 获取答案参考来源 |
| `GET`  | `/api/health` | — | 健康检查 |

### 上传文档

```bash
curl -X POST http://localhost:8080/api/documents/upload \
  -F "file=@example.pdf"
```

响应示例：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "fileName": "example.pdf",
    "fileType": "pdf",
    "fileSize": 102400,
    "chunkCount": 15,
    "uploadTime": "2024-01-01T12:00:00"
  }
}
```

### SSE 流式问答

```bash
curl -X POST http://localhost:8080/api/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"question": "这份文档的核心观点是什么？"}'
```

响应为 `text/event-stream` 流，前端自动渲染打字机效果：

```
data:根据
data:参考
data:资料
data:，这份文档
data:的核心观点是...
data:[DONE]
```

### 获取来源

```bash
curl -X POST http://localhost:8080/api/chat/sources \
  -H "Content-Type: application/json" \
  -d '{"question": "核心观点"}'
```

```json
{
  "code": 200,
  "data": [
    {
      "documentName": "example.pdf",
      "content": "本文的核心观点是...",
      "similarity": 0.92
    }
  ]
}
```

## 🔌 扩展向量库

### 切换到 Chroma

1. 安装依赖：

```bash
pip install chromadb
```

2. 修改 `ai-rag-py/services/vector_store_service.py`：

```python
from langchain_chroma import Chroma

def get_vector_store():
    global _vector_store
    if _vector_store is None:
        embeddings = _get_embeddings()
        _vector_store = Chroma(
            embedding_function=embeddings,
            persist_directory="./chroma_db",
        )
    return _vector_store
```

### 切换到 PGVector

1. 安装依赖：

```bash
pip install pgvector psycopg2-binary
```

2. 替换 `vector_store_service.py` 中的向量库为 `PGVector` 即可。

### 其他向量库

LangChain 支持 FAISS、Chroma、PGVector、Milvus、Weaviate、Pinecone 等，替换方式类似，修改 `vector_store_service.py` 中的实现即可。

## 🏗️ 技术栈

| 层级 | 技术 |
|------|------|
| **后端框架** | FastAPI |
| **AI 引擎** | LangChain + langchain-openai |
| **文档解析** | PyPDFLoader / TextLoader |
| **文本分块** | RecursiveCharacterTextSplitter |
| **向量库** | FAISS（默认）/ Chroma / PGVector / Milvus |
| **流式输出** | FastAPI StreamingResponse + AsyncGenerator |
| **前端框架** | Vue 3 + TypeScript |
| **构建工具** | Vite 5 |
| **UI 组件** | Element Plus 2.7 |
| **Markdown 渲染** | marked + highlight.js |
| **HTTP 客户端** | Axios + Fetch API |


## 📄 License

MIT

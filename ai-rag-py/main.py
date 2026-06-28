"""
 AI RAG 知识库问答 —— Python + LangChain 版 主入口

启动命令:
    uvicorn main:app --host 0.0.0.0 --port 8080 --reload

"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import documents, chat

# ─── 日志配置 ───
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)

# ─── FastAPI 应用 ───
app = FastAPI(
    title="AI RAG 知识库问答",
    description="基于 LangChain + FAISS 的 RAG 知识库问答系统",
    version="1.0.0",
)

# ─── CORS 跨域（允许前端开发服务器访问） ───
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── 注册路由 ───
app.include_router(documents.router)
app.include_router(chat.router)


# ─── 健康检查 ───
@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "AI RAG (Python + LangChain)"}

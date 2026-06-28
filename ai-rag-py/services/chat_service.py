"""
RAG 对话服务 —— 检索增强生成 + 流式输出 + 来源标注
"""

import logging
from typing import AsyncGenerator, List

from langchain_core.documents import Document
from langchain_openai import ChatOpenAI

from config import config
from models import SourceSegment
from services.vector_store_service import search_similar, build_context
from utils.prompt import build_rag_prompt

logger = logging.getLogger(__name__)


def _get_llm(streaming: bool = True) -> ChatOpenAI:
    """获取大模型客户端"""
    mc = config.active_model_config
    return ChatOpenAI(
        model=mc.chat_model,
        base_url=mc.base_url,
        api_key=mc.api_key,
        temperature=0.7,
        streaming=streaming,
    )


async def chat_stream(question: str) -> AsyncGenerator[str, None]:
    """
    RAG 知识库问答 —— SSE 流式输出

    Args:
        question: 用户问题

    Yields:
        SSE 格式的文本片段
    """
    # 1. 检索相关文档
    docs_with_scores = search_similar(question)

    # 2. 构建上下文
    context = build_context(docs_with_scores)

    # 3. 构建 Prompt
    prompt_content = build_rag_prompt(question, context)

    # 4. 流式调用大模型
    llm = _get_llm(streaming=True)
    try:
        async for chunk in llm.astream(prompt_content):
            if chunk.content:
                yield f"data:{chunk.content}\n\n"
    except Exception as e:
        logger.error("流式对话异常: %s", e)
        yield f"data:[错误] {str(e)}\n\n"

    yield "data:[DONE]\n\n"


def extract_sources(question: str) -> List[SourceSegment]:
    """
    提取答案参考来源

    Args:
        question: 用户问题

    Returns:
        来源片段列表
    """
    docs_with_scores = search_similar(question)

    sources = []
    for doc, score in docs_with_scores:
        content = doc.page_content
        sources.append(SourceSegment(
            documentName=doc.metadata.get("file_name", "未知"),
            content=content[:300] + ("..." if len(content) > 300 else ""),
            similarity=round(score, 4),
        ))

    return sources

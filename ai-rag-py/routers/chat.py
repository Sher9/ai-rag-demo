"""
对话路由 —— POST /api/chat/stream（SSE）, POST /api/chat/sources
"""

import logging

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import ValidationError

from models import R, ChatRequest, SourceSegment
from services.chat_service import chat_stream, extract_sources

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/chat", tags=["知识库问答"])


@router.post("/stream")
async def chat_stream_endpoint(request: ChatRequest):
    """
    SSE 流式问答

    返回 text/event-stream 格式，前端通过 fetch + ReadableStream 读取
    """
    logger.info("收到流式问答请求: %s", request.question)

    return StreamingResponse(
        chat_stream(request.question),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/sources")
async def get_sources_endpoint(request: ChatRequest) -> R:
    """获取答案来源片段"""
    try:
        sources = extract_sources(request.question)
        return R.ok(sources)
    except Exception as e:
        logger.error("获取来源失败: %s", e, exc_info=True)
        return R.fail(f"获取来源失败: {str(e)}")

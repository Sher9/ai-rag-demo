"""
Pydantic 响应模型 —— 与前端 DTO 完全对齐
"""

from datetime import datetime
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


# ─── 统一响应 ───

class R(BaseModel, Generic[T]):
    code: int = 200
    message: str = "success"
    data: Optional[T] = None

    @staticmethod
    def ok(data: T = None) -> "R":
        return R(code=200, message="success", data=data)

    @staticmethod
    def fail(msg: str, code: int = 500) -> "R":
        return R(code=code, message=msg, data=None)


# ─── 文档信息 ───

class DocumentVO(BaseModel):
    id: Optional[str] = None
    fileName: str = ""
    fileType: str = ""
    fileSize: int = 0
    chunkCount: int = 0
    uploadTime: Optional[datetime] = Field(default_factory=datetime.now)


# ─── 对话请求 ───

class ChatRequest(BaseModel):
    question: str
    conversationId: Optional[str] = None


# ─── 来源片段 ───

class SourceSegment(BaseModel):
    documentName: str = ""
    content: str = ""
    similarity: float = 0.0

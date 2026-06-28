"""
文档管理路由 —— POST /api/documents/upload
"""

import os
import tempfile
import logging

from fastapi import APIRouter, UploadFile, File

from models import R, DocumentVO
from services.document_service import process_document

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/documents", tags=["文档管理"])


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)) -> R:
    """
    上传文档并自动向量化入库

    支持格式: PDF / TXT / Markdown / Word
    """
    if not file.filename:
        return R.fail("文件不能为空")

    logger.info("收到上传文件: %s (%d bytes)", file.filename, file.size or 0)

    # 保存到临时文件
    suffix = os.path.splitext(file.filename)[1] or ".tmp"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        chunk_count = process_document(tmp_path, file.filename)

        vo = DocumentVO(
            fileName=file.filename,
            fileType=_get_file_type(file.filename),
            fileSize=file.size or len(content),
            chunkCount=chunk_count,
        )
        return R.ok(vo)
    except Exception as e:
        logger.error("文档处理失败: %s", e, exc_info=True)
        return R.fail(f"文档处理失败: {str(e)}")
    finally:
        # 清理临时文件
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def _get_file_type(filename: str) -> str:
    """根据文件扩展名返回类型标识"""
    if not filename:
        return "unknown"
    ext = os.path.splitext(filename)[1].lower()
    mapping = {
        ".pdf": "pdf",
        ".txt": "txt",
        ".md": "markdown",
        ".markdown": "markdown",
        ".doc": "word",
        ".docx": "word",
    }
    return mapping.get(ext, "other")

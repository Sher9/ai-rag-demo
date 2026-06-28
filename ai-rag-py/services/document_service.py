"""
文档处理服务 —— 读取 → 分块 → 向量化 → 入库
支持 PDF / TXT / Markdown 等格式
"""

import uuid
import logging
from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from config import config

logger = logging.getLogger(__name__)


def _load_file(file_path: str, original_name: str) -> List[Document]:
    """根据文件类型选择合适的加载器"""
    suffix = Path(original_name).suffix.lower()
    logger.info("加载文档: %s (类型: %s)", original_name, suffix)

    if suffix == ".pdf":
        loader = PyPDFLoader(file_path)
        docs = loader.load()
    elif suffix in (".txt", ".md", ".markdown"):
        loader = TextLoader(file_path, encoding="utf-8")
        docs = loader.load()
    elif suffix in (".doc", ".docx"):
        # Word 文档：尝试使用 TextLoader，或提示安装 docx2txt
        try:
            loader = TextLoader(file_path, encoding="utf-8")
            docs = loader.load()
        except Exception:
            raise ValueError(
                "Word 文档需要安装 python-docx: pip install docx2txt"
            )
    else:
        # 兜底：尝试 TextLoader
        try:
            loader = TextLoader(file_path, encoding="utf-8")
            docs = loader.load()
        except Exception:
            raise ValueError(f"不支持的文件格式: {suffix}")

    logger.info("文档 %s 原始加载 %d 个 Document", original_name, len(docs))
    return docs


def process_document(file_path: str, original_name: str) -> int:
    """
    处理上传的文档：加载 → 分块 → 向量化 → 入库

    Args:
        file_path: 临时文件路径
        original_name: 原始文件名

    Returns:
        产生的文档块数量
    """
    from services.vector_store_service import get_vector_store, add_documents

    # 1. 加载文档
    documents = _load_file(file_path, original_name)
    if not documents:
        logger.warning("文档内容为空: %s", original_name)
        return 0

    # 2. 添加元数据
    doc_id = uuid.uuid4().hex[:8]
    for doc in documents:
        doc.metadata["doc_id"] = doc_id
        doc.metadata["file_name"] = original_name
        doc.metadata["source"] = original_name

    # 3. 文本分块
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.chunk.chunk_size,
        chunk_overlap=config.chunk.chunk_overlap,
        separators=["\n\n", "\n", "。", ".", " ", ""],
    )
    chunks = splitter.split_documents(documents)

    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = str(i)

    logger.info("文档 %s 分为 %d 个块", original_name, len(chunks))

    # 4. 向量化并入库
    if chunks:
        add_documents(chunks)

    logger.info("文档 %s 处理完成，已入库 %d 个块", original_name, len(chunks))
    return len(chunks)

"""
向量库服务 —— FAISS 内存向量库，开箱即跑
可替换为 Chroma / PGVector / Milvus
"""

import logging
from typing import List, Tuple

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from config import config

logger = logging.getLogger(__name__)

# 全局向量库实例
_vector_store: FAISS | None = None


def _get_embeddings() -> OpenAIEmbeddings:
    """获取 Embeddings 模型"""
    mc = config.active_model_config
    return OpenAIEmbeddings(
        model=mc.embedding_model,
        base_url=mc.base_url,
        api_key=mc.api_key,
    )


def get_vector_store() -> FAISS:
    """获取（或初始化）向量库"""
    global _vector_store
    if _vector_store is None:
        embeddings = _get_embeddings()
        # 用一个空文档初始化 FAISS，后续通过 add_documents 追加
        dummy = Document(page_content="__init__", metadata={})
        _vector_store = FAISS.from_documents([dummy], embeddings)
        logger.info("FAISS 向量库初始化完成")
    return _vector_store


def add_documents(documents: List[Document]) -> None:
    """添加文档到向量库"""
    store = get_vector_store()
    store.add_documents(documents)
    logger.info("已添加 %d 个文档块到向量库", len(documents))


def search_similar(query: str) -> List[Tuple[Document, float]]:
    """
    语义检索相关文档片段

    Returns:
        List of (Document, similarity_score)，按相似度降序排列
    """
    store = get_vector_store()
    top_k = config.retrieval.top_k
    threshold = config.retrieval.similarity_threshold

    # FAISS 返回 (Document, distance)，distance 越低越相似
    results_with_distance = store.similarity_search_with_score(query, k=top_k)

    # 将 L2 距离转换为相似度分数 (0~1)
    scored: List[Tuple[Document, float]] = []
    for doc, distance in results_with_distance:
        sim = 1.0 / (1.0 + distance)  # L2 → 相似度
        if sim >= threshold:
            doc.metadata["_similarity"] = str(sim)
            scored.append((doc, sim))

    logger.info("检索完成，查询: %s，命中 %d 条 (共 %d 条候选)",
                query[:50], len(scored), len(results_with_distance))
    return scored


def build_context(docs_with_scores: List[Tuple[Document, float]]) -> str:
    """构建上下文文本（用于拼接 Prompt）"""
    if not docs_with_scores:
        return ""

    parts = []
    for doc, _score in docs_with_scores:
        file_name = doc.metadata.get("file_name", "未知")
        content = doc.page_content
        parts.append(f"【来源：{file_name}】\n{content}")

    return "\n\n---\n\n".join(parts)

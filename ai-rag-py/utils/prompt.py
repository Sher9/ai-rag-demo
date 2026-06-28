"""
RAG Prompt 模板
"""

RAG_SYSTEM_PROMPT = """你是一个知识库问答助手。请根据以下参考资料回答用户问题。

## 规则
1. 仅根据参考资料回答，不要编造信息
2. 如果参考资料中找不到答案，请明确告知用户
3. 回答应简洁、准确、有条理
4. 在回答末尾可以标注信息来源

## 参考资料
{context}

## 用户问题
{question}

## 回答
"""


def build_rag_prompt(question: str, context: str) -> str:
    """构建 RAG Prompt"""
    ctx = context if context.strip() else "（暂无相关参考资料）"
    return RAG_SYSTEM_PROMPT.format(context=ctx, question=question)

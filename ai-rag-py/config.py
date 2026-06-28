"""
核心配置模块 —— 一切配置的入口
切换模型只需修改 active_model 字段值：
  deepseek | doubao | qwen
"""

import os
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class ModelConfig:
    """单个模型的配置"""
    base_url: str
    api_key: str
    chat_model: str
    embedding_model: str


@dataclass
class ChunkConfig:
    """文档分块配置"""
    chunk_size: int = 800
    chunk_overlap: int = 100


@dataclass
class RetrievalConfig:
    """检索配置"""
    top_k: int = 4
    similarity_threshold: float = 0.7


@dataclass
class AppConfig:
    """应用总配置"""
    active_model: str = "deepseek"

    chunk: ChunkConfig = field(default_factory=ChunkConfig)
    retrieval: RetrievalConfig = field(default_factory=RetrievalConfig)

    models: Dict[str, ModelConfig] = field(default_factory=lambda: {
        "deepseek": ModelConfig(
            base_url="https://api.deepseek.com",
            api_key=os.getenv("DEEPSEEK_API_KEY", "sk-deepseek"),
            chat_model="deepseek-chat",
            embedding_model="text-embedding-ada-002",
        ),
        "doubao": ModelConfig(
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            api_key=os.getenv("DOUBAO_API_KEY", "your-doubao-api-key"),
            chat_model="your-doubao-endpoint-id",
            embedding_model="your-doubao-embedding-endpoint-id",
        ),
        "qwen": ModelConfig(
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            api_key=os.getenv("QWEN_API_KEY", "sk-your-qwen-api-key"),
            chat_model="qwen-plus",
            embedding_model="text-embedding-v2",
        ),
    })

    @property
    def active_model_config(self) -> ModelConfig:
        """获取当前激活的模型配置"""
        if self.active_model not in self.models:
            raise ValueError(
                f"未知模型: {self.active_model}，可选值: {list(self.models.keys())}"
            )
        return self.models[self.active_model]


# 全局单例
config = AppConfig()

import logging

from llama_index import MockEmbedding
from llama_index.embeddings.base import BaseEmbedding

from app._config import settings
from app.enums import EmbeddingMode
from app.paths import models_cache_path

logger = logging.getLogger(__name__)

MOCK_EMBEDDING_DIM = 1536


class EmbeddingComponent:
    embedding_model: BaseEmbedding

    def __init__(self) -> None:
        embedding_mode = settings.EMBEDDING_MODE
        logger.info("Initializing the embedding model in mode=%s", embedding_mode)
        match embedding_mode:
            case EmbeddingMode.OPENAI:
                from llama_index import OpenAIEmbedding

                self.embedding_model = OpenAIEmbedding(api_key=settings.OPENAI_API_KEY)

            case EmbeddingMode.MOCK:
                # Not a random number, is the dimensionality used by
                # the default embedding model
                self.embedding_model = MockEmbedding(MOCK_EMBEDDING_DIM)

            case EmbeddingMode.LOCAL:
                from llama_index.embeddings import HuggingFaceEmbedding

                self.embedding_model = HuggingFaceEmbedding(
                    model_name=settings.LOCAL_HF_EMBEDDING_MODEL_NAME,
                    cache_folder=str(models_cache_path),
                )

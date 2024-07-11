import logging
import typing

from llama_index import VectorStoreIndex
from llama_index.indices.vector_store import VectorIndexRetriever
from llama_index.vector_stores.types import VectorStore

from app._config import settings
from app.enums import WEAVIATE_INDEX_NAME, VectorDatabase

logger = logging.getLogger(__name__)


class VectorStoreComponent:
    vector_store: VectorStore

    def __init__(self) -> None:
        match settings.VECTOR_DATABASE:
            case VectorDatabase.WEAVIATE:
                import weaviate
                from llama_index.vector_stores import WeaviateVectorStore

                if settings.WCS_URL and settings.WCS_API_KEY:
                    client = weaviate.Client(
                        url=settings.WCS_URL,
                        auth_client_secret=weaviate.auth.AuthApiKey(
                            api_key=settings.WCS_API_KEY
                        ),  # Replace with your Weaviate instance API key
                        additional_headers={
                            "X-OpenAI-Api-key": settings.OPENAI_API_KEY  # Replace with your third party API key and identifying header
                        },
                    )
                    logger.info("Connected to Weaviate cloud with WCS credentials...")
                else:
                    client = weaviate.Client(settings.WEAVIATE_CLIENT_URL)
                    logger.info("Connected to Weaviate self host...")

                self.vector_store = typing.cast(
                    VectorStore,
                    WeaviateVectorStore(
                        weaviate_client=client, index_name=WEAVIATE_INDEX_NAME
                    ),
                )
            case _:
                # Should be unreachable
                # The settings validator should have caught this
                raise ValueError(
                    f"Vectorstore database {settings.VECTOR_DATABASE} not supported"
                )

    @staticmethod
    def get_retriever(
        index: VectorStoreIndex,
        doc_ids: list[str] | None = None,
        similarity_top_k: int = 2,
    ) -> VectorIndexRetriever:
        return VectorIndexRetriever(
            index=index,
            similarity_top_k=similarity_top_k,
            doc_ids=doc_ids,
        )

    def close(self) -> None:
        if hasattr(self.vector_store.client, "close"):
            self.vector_store.client.close()

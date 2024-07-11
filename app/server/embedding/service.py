from app.components.embedding.component import EmbeddingComponent
from app.server.embedding.schemas import Embedding


class EmbeddingsService:
    def __init__(self, embedding_component: EmbeddingComponent) -> None:
        self.embedding_model = embedding_component.embedding_model

    def embed_texts(self, texts: list[str]) -> list[Embedding]:
        texts_embeddings = self.embedding_model.get_text_embedding_batch(texts)
        return [
            Embedding(
                index=texts_embeddings.index(embedding),
                object="embedding",
                embedding=embedding,
            )
            for embedding in texts_embeddings
        ]

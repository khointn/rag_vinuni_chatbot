from fastapi import APIRouter

from app.components.embedding.component import EmbeddingComponent
from app.server.embedding.schemas import EmbeddingsBody, EmbeddingsResponse
from app.server.embedding.service import EmbeddingsService

embedding_router = APIRouter()


@embedding_router.post("/embedding", tags=["Embeddings"])
def generate_embeddings(body: EmbeddingsBody) -> EmbeddingsResponse:
    embedding_component = EmbeddingComponent()
    service = EmbeddingsService(embedding_component)
    input_texts = body.input if isinstance(body.input, list) else [body.input]
    embeddings = service.embed_texts(input_texts)
    return EmbeddingsResponse(
        object="list", model=service.embedding_model.model_name, data=embeddings
    )

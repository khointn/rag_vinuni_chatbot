import logging

from fastapi import FastAPI

from app._config import settings
from app.components.embedding.component import EmbeddingComponent
from app.components.llm.component import LLMComponent
from app.components.node_store.component import NodeStoreComponent
from app.components.vector_store.component import VectorStoreComponent
from app.server.chat.router import chat_router
from app.server.chat.service import ChatService
from app.server.embedding.router import embedding_router
from app.server.ingest.service import IngestService

logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(chat_router)
app.include_router(embedding_router)

# if settings.IS_UI_ENABLED:
#     logger.debug("Importing the UI module")
#     from app.ui.ui import PrivateGptUi

#     llm_component = LLMComponent()
#     vector_store_component = VectorStoreComponent()
#     embedding_component = EmbeddingComponent()
#     node_store_component = NodeStoreComponent()

#     ingest_service = IngestService(
#         llm_component, vector_store_component, embedding_component, node_store_component
#     )
#     chat_service = ChatService(
#         llm_component, vector_store_component, embedding_component, node_store_component
#     )

#     ui = PrivateGptUi(ingest_service, chat_service)
#     ui.mount_in_app(app, settings.UI_PATH)

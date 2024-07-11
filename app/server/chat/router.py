from fastapi import APIRouter
from llama_index.llms import ChatMessage, MessageRole
from pydantic import BaseModel

from app.components.embedding.component import EmbeddingComponent
from app.components.llm.component import LLMComponent
from app.components.node_store.component import NodeStoreComponent
from app.components.vector_store.component import VectorStoreComponent
from app.server.chat.service import ChatService
from app.server.chat.utils import OpenAICompletion, OpenAIMessage, to_openai_response

chat_router = APIRouter()


class ChatBody(BaseModel):
    messages: list[OpenAIMessage]
    include_sources: bool = True

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a rapper. Always answer with a rap.",
                        },
                        {
                            "role": "user",
                            "content": "How do you fry an egg?",
                        },
                    ],
                    "include_sources": True,
                }
            ]
        }
    }


@chat_router.post(
    "/chat",
    response_model=None,
    responses={200: {"model": OpenAICompletion}},
    tags=["Contextual Completions"],
)
def chat_completion(body: ChatBody) -> OpenAICompletion:
    """Given a list of messages comprising a conversation, return a response.

    Optionally include an initial `role: system` message to influence the way
    the LLM answers.

    When using `'include_sources': true`, the API will return the source Chunks used
    to create the response, which come from the context provided.
    """
    llm_component = LLMComponent()
    vector_store_component = VectorStoreComponent()
    embedding_component = EmbeddingComponent()
    node_store_component = NodeStoreComponent()

    chat_service = ChatService(
        llm_component, vector_store_component, embedding_component, node_store_component
    )
    all_messages = [
        ChatMessage(content=m.content, role=MessageRole(m.role)) for m in body.messages
    ]

    completion = chat_service.chat(messages=all_messages)
    return to_openai_response(
        completion.response, completion.sources if body.include_sources else None
    )

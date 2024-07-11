from dataclasses import dataclass

from llama_index import ServiceContext, StorageContext, VectorStoreIndex
from llama_index.chat_engine import ContextChatEngine
from llama_index.chat_engine.types import BaseChatEngine
from llama_index.indices.postprocessor import MetadataReplacementPostProcessor
from llama_index.llms import ChatMessage, MessageRole
from llama_index.memory import ChatMemoryBuffer

from app.components.embedding.component import EmbeddingComponent
from app.components.llm.component import LLMComponent
from app.components.node_store.component import NodeStoreComponent
from app.components.vector_store.component import VectorStoreComponent
from app.server.chat.schemas import Chunk, Completion


@dataclass
class ChatEngineInput:
    system_message: ChatMessage | None = None
    last_message: ChatMessage | None = None
    chat_history: list[ChatMessage] | None = None

    @classmethod
    def from_messages(cls, messages: list[ChatMessage]) -> "ChatEngineInput":
        # Detect if there is a system message, extract the last message and chat history
        system_message = (
            messages[0]
            if len(messages) > 0 and messages[0].role == MessageRole.SYSTEM
            else None
        )
        last_message = (
            messages[-1]
            if len(messages) > 0 and messages[-1].role == MessageRole.USER
            else None
        )
        # Remove from messages list the system message and last message,
        # if they exist. The rest is the chat history.
        if system_message:
            messages.pop(0)
        if last_message:
            messages.pop(-1)
        chat_history = messages if len(messages) > 0 else None

        return cls(
            system_message=system_message,
            last_message=last_message,
            chat_history=chat_history,
        )


class ChatService:
    def __init__(
        self,
        llm_component: LLMComponent,
        vector_store_component: VectorStoreComponent,
        embedding_component: EmbeddingComponent,
        node_store_component: NodeStoreComponent,
    ) -> None:
        self.llm_service = llm_component
        self.vector_store_component = vector_store_component
        self.storage_context = StorageContext.from_defaults(
            vector_store=vector_store_component.vector_store,
            docstore=node_store_component.doc_store,
            index_store=node_store_component.index_store,
        )
        self.service_context = ServiceContext.from_defaults(
            llm=llm_component.llm, embed_model=embedding_component.embedding_model
        )
        self.index = VectorStoreIndex.from_vector_store(
            vector_store_component.vector_store,
            storage_context=self.storage_context,
            service_context=self.service_context,
            show_progress=True,
        )

    def _chat_engine(self, system_prompt: str | None = None) -> BaseChatEngine:
        vector_index_retriever = self.vector_store_component.get_retriever(
            index=self.index
        )

        memory = ChatMemoryBuffer.from_defaults(token_limit=16000)  # <-- MORE TOKENS

        return ContextChatEngine.from_defaults(
            system_prompt=system_prompt,
            retriever=vector_index_retriever,
            memory=memory,
            service_context=self.service_context,
            node_postprocessors=[
                MetadataReplacementPostProcessor(target_metadata_key="window"),
            ],
        )

    def chat(self, messages: list[ChatMessage]):
        chat_engine_input = ChatEngineInput.from_messages(messages)
        last_message = (
            chat_engine_input.last_message.content
            if chat_engine_input.last_message
            else None
        )
        system_prompt = (
            chat_engine_input.system_message.content
            if chat_engine_input.system_message
            else None
        )
        chat_history = (
            chat_engine_input.chat_history if chat_engine_input.chat_history else None
        )

        chat_engine = self._chat_engine(system_prompt=system_prompt)
        wrapped_response = chat_engine.chat(
            message=last_message if last_message is not None else "",
            chat_history=chat_history,
        )

        sources = [Chunk.from_node(node) for node in wrapped_response.source_nodes]
        completion = Completion(response=wrapped_response.response, sources=sources)
        return completion

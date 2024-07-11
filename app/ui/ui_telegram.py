"""This file should be imported only and only if you want to run the UI locally."""

import itertools
import logging
import os
import subprocess
from pathlib import Path
from typing import Any
import sys
sys.path.append('/home/khointn/llm-vinunibot/')

from llama_index.llms import ChatMessage, MessageRole
from telebot import TeleBot

from app._config import settings
from app.components.embedding.component import EmbeddingComponent
from app.components.llm.component import LLMComponent
from app.components.node_store.component import NodeStoreComponent
from app.components.vector_store.component import VectorStoreComponent
from app.enums import PROJECT_ROOT_PATH
from app.paths import local_data_path
from app.server.chat.service import ChatService
from app.ui.schemas import Source

logger = logging.getLogger(__name__)

THIS_DIRECTORY_RELATIVE = Path(__file__).parent.relative_to(PROJECT_ROOT_PATH)
AVATAR_BOT = THIS_DIRECTORY_RELATIVE / "dodge_ava.jpg"

UI_TAB_TITLE = "VinUni Chatbot"

SOURCES_SEPARATOR = "\n\n Sources: \n"


class TelegramBot:
    def __init__(
        self,
        chat_service: ChatService,
    ) -> None:
        self._chat_service = chat_service
        # Initialize system prompt
        self._system_prompt = self._get_default_system_prompt()

    def chat(
        self,
        message: str,
        history: list[list[str]],
        # show_image: bool,
    ) -> Any:
        # logger.info(f"Show image = {show_image}")

        def build_history() -> list[ChatMessage]:
            history_messages: list[ChatMessage] = list(
                itertools.chain(
                    *[
                        [
                            ChatMessage(content=interaction[0], role=MessageRole.USER),
                            ChatMessage(
                                # Remove from history content the Sources information
                                content=(
                                    "[Image Output]"
                                    if isinstance(interaction[1], tuple)
                                    else (interaction[1]).split(SOURCES_SEPARATOR)[0]
                                ),
                                role=MessageRole.ASSISTANT,
                            ),
                        ]
                        for interaction in history
                    ]
                )
            )

            # max 20 messages to try to avoid context overflow
            return history_messages[:20]

        new_message = ChatMessage(content=message, role=MessageRole.USER)
        all_messages = [*build_history(), new_message]
        # If a system prompt is set, add it as a system message
        if self._system_prompt:
            all_messages.insert(
                0,
                ChatMessage(
                    content=self._system_prompt,
                    role=MessageRole.SYSTEM,
                ),
            )

        completion = self._chat_service.chat(messages=all_messages)

        text_sources = []
        for source in completion.sources:
            text_sources.append(source.text)

        # with open("/home/khointn/llm-vinunibot/test.txt", "w+") as f:
        #     f.write(str(text_sources))
        #     f.close()

        print("Source: ", text_sources)
        full_response = completion.response

        # if completion.sources:
        #     full_response += SOURCES_SEPARATOR
        #     curated_sources = Source.curate_sources(completion.sources)
        #     sources_text = "\n\n\n".join(
        #         f"{index}. {source.file} (page {source.page})"
        #         for index, source in enumerate(curated_sources, start=1)
        #     )
        #     full_response += sources_text

        return full_response

    # On initialization this function set the system prompt
    # to the default prompt based on settings.
    @staticmethod
    def _get_default_system_prompt() -> str:
        return settings.DEFAULT_QUERY_SYSTEM_PROMPT

    def _set_system_prompt(self, system_prompt_input: str) -> None:
        logger.info(f"Setting system prompt to: {system_prompt_input}")
        self._system_prompt = system_prompt_input


if __name__ == "__main__":
    llm_component = LLMComponent()
    vector_store_component = VectorStoreComponent()
    embedding_component = EmbeddingComponent()
    node_store_component = NodeStoreComponent()

    chat_service = ChatService(
        llm_component, vector_store_component, embedding_component, node_store_component
    )

    tele_bot = TelegramBot(chat_service)
    bot = TeleBot(token=settings.TELEGRAM_BOT_API, parse_mode=None)

    @bot.message_handler(commands=["start"])
    def send_welcome(message):
        bot.send_message(
            message.chat.id, "Xin chào! VinUni Admission Support có thể giúp gì cho bạn?"
        )

    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        # Simulate chat history (you might want to store the history properly)
        chat_history = []
        # Process the message through your chat system

        print("Question: ", message.text)
        response = tele_bot.chat(message.text, chat_history)
        print(f"RESPONSE: {response}")
        # Send the response back to the user

        bot.reply_to(message, response)

    bot.infinity_polling(allowed_updates=["message", "message_reaction"])

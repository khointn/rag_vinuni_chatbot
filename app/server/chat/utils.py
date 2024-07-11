import time
import uuid
from typing import Literal

from llama_index.llms import ChatResponse
from pydantic import BaseModel, Field

from app.server.chat.schemas import Chunk


class OpenAIMessage(BaseModel):
    """Inference result, with the source of the message.

    Role could be the assistant or system
    (providing a default response, not AI generated).
    """

    role: Literal["assistant", "system", "user"] = Field(default="user")
    content: str | None


class OpenAIChoice(BaseModel):
    """Response from AI."""

    finish_reason: str | None = Field(examples=["stop"])
    message: OpenAIMessage | None = None
    sources: list[Chunk] | None = None
    index: int = 0


class OpenAICompletion(BaseModel):
    """Clone of OpenAI Completion model.

    For more information see: https://platform.openai.com/docs/api-reference/chat/object
    """

    id: str
    object: Literal["completion", "completion.chunk"] = Field(default="completion")
    created: int = Field(..., examples=[1623340000])
    model: Literal["llm-vinunibot"]
    choices: list[OpenAIChoice]

    @classmethod
    def from_text(
        cls,
        text: str | None,
        finish_reason: str | None = None,
        sources: list[Chunk] | None = None,
    ) -> "OpenAICompletion":
        return OpenAICompletion(
            id=str(uuid.uuid4()),
            object="completion",
            created=int(time.time()),
            model="llm-vinunibot",
            choices=[
                OpenAIChoice(
                    message=OpenAIMessage(role="assistant", content=text),
                    finish_reason=finish_reason,
                    sources=sources,
                )
            ],
        )


def to_openai_response(
    response: str | ChatResponse, sources: list[Chunk] | None = None
) -> OpenAICompletion:
    return OpenAICompletion.from_text(response, finish_reason="stop", sources=sources)

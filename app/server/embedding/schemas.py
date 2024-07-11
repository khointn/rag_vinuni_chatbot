from typing import Literal

from pydantic import BaseModel, Field


class Embedding(BaseModel):
    index: int
    object: Literal["embedding"]
    embedding: list[float] = Field(examples=[[0.1, -0.2]])


class EmbeddingsBody(BaseModel):
    input: str | list[str]


class EmbeddingsResponse(BaseModel):
    object: Literal["list"]
    model: str
    data: list[Embedding]

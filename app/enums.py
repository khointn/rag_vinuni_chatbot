from enum import Enum, auto, unique
from pathlib import Path

PROJECT_ROOT_PATH: Path = Path(__file__).parents[1]


@unique
class BaseEnum(str, Enum):
    @staticmethod
    def _generate_next_value_(name: str, *_):
        """
        Automatically generate values for enum.
        Enum values are lower-cased enum member names.
        """
        return name.lower()

    @classmethod
    def get_values(cls) -> list[str]:
        # noinspection PyUnresolvedReferences
        return [m.value for m in cls]


class LLMMode(BaseEnum):
    MOCK = auto()
    OPENAI = auto()
    LOCAL = auto()


class EmbeddingMode(BaseEnum):
    MOCK = auto()
    OPENAI = auto()
    LOCAL = auto()


class VectorDatabase(BaseEnum):
    WEAVIATE = auto()


WEAVIATE_INDEX_NAME = "VinUniWebdata"

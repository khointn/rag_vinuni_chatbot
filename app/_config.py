import os
from typing import Literal, Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str
    PORT: int = 8000
    VECTOR_DATABASE: Literal["weaviate"] = "weaviate"

    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-3.5-turbo"

    WEAVIATE_CLIENT_URL: str = "http://localhost:8080"
    WCS_URL: Optional[str] = None
    WCS_API_KEY: Optional[str] = None

    TELEGRAM_BOT_API: str = None

    LLM_MODE: Literal["openai", "mock", "local"] = "openai"
    EMBEDDING_MODE: Literal["openai", "mock", "local"] = "openai"

    LOCAL_DATA_FOLDER: str = "local_data/test"

    DEFAULT_QUERY_SYSTEM_PROMPT: str = "Đóng vai một chuyên viên tư vấn tuyển sinh cho trường Đại học VinUni ở Việt Nam. \
    Hãy giúp trả lời các câu hỏi từ phụ huynh và học sinh dựa trên dữ liệu được cung cấp. \
    Chỉ được phép trả lời dựa trên dữ liệu được cung cấp. Không được phép tự ý đưa ra câu trả lời khi không có dữ liệu.\
    Nếu không có dữ liệu, trả lời 'Chúng tôi sẽ liên hệ với bạn sau'.\
    Nếu được hỏi những câu hỏi về đại học khác, trả lời 'Xin hãy liên hệ với đại học bạn cần tham khảo để tìm kiếm thông tin'"
    
    # "You are an admissions consultant for VinUniversity in Vietnam. \
    #     Answer questions from parents and students based on the data provided. \
    #     Only answer based on the data provided. Do not provide answers without data. \
    #     If there is no data, respond with 'We will contact you later'. \
    #     If asked questions about other universities, respond with 'Please contact the university you are inquiring about for more information'."

    LOCAL_HF_EMBEDDING_MODEL_NAME: str = "BAAI/bge-small-en-v1.5"

    LOCAL_HF_LLM_REPO_ID: str = "TheBloke/Llama-2-7B-Chat-GGUF"
    LOCAL_HF_LLM_MODEL_FILE: str = "llama-2-7b-chat.Q4_K_M.gguf"

    # LLM config
    LLM_TEMPERATURE: float = Field(
        default=0.1, description="The temperature to use for sampling."
    )
    LLM_MAX_NEW_TOKENS: int = Field(
        default=256,
        description="The maximum number of tokens to generate.",
    )
    LLM_CONTEXT_WINDOW: int = Field(
        default=3900,
        description="The maximum number of context tokens for the model.",
    )

    # UI
    IS_UI_ENABLED: bool = True
    UI_PATH: str = "/"

    class Config:
        case_sensitive = True
        env_file_encoding = "utf-8"


environment = os.environ.get("ENVIRONMENT", "local")
settings = Settings(
    ENVIRONMENT=environment,
    # ".env.{environment}" takes priority over ".env"
    _env_file=[".env", f".env.{environment}"],
)

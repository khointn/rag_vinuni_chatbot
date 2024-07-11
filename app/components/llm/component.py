import logging

from llama_index.llms import LLM, MockLLM

from app._config import settings
from app.enums import LLMMode
from app.paths import models_path

logger = logging.getLogger(__name__)


class LLMComponent:
    llm: LLM

    def __init__(self) -> None:
        llm_mode = settings.LLM_MODE
        logger.info(f"Initializing the LLM in mode={llm_mode}")
        match settings.LLM_MODE:
            case LLMMode.OPENAI:
                from llama_index.llms import OpenAI

                self.llm = OpenAI(
                    api_key=settings.OPENAI_API_KEY,
                    model=settings.OPENAI_MODEL,
                )
            case LLMMode.MOCK:
                self.llm = MockLLM()

            case LLMMode.LOCAL:
                from llama_index.llms import LlamaCPP
                from llama_index.llms.llama_utils import (
                    completion_to_prompt,
                    messages_to_prompt,
                )

                self.llm = LlamaCPP(
                    model_path=str(models_path / settings.LOCAL_HF_LLM_MODEL_FILE),
                    temperature=settings.LLM_TEMPERATURE,
                    max_new_tokens=settings.LLM_MAX_NEW_TOKENS,
                    context_window=settings.LLM_CONTEXT_WINDOW,
                    generate_kwargs={},
                    # set to at least 1 to use GPU
                    # set to -1 for all gpu
                    # set to 0 for cpu
                    model_kwargs={"n_gpu_layers": 1},
                    # transform inputs into Llama2 format
                    messages_to_prompt=messages_to_prompt,
                    completion_to_prompt=completion_to_prompt,
                    verbose=True,
                )

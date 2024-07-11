import logging
import os

from huggingface_hub import hf_hub_download, snapshot_download

from app._config import settings
from app.paths import models_cache_path, models_path

os.makedirs(models_path, exist_ok=True)

logger = logging.getLogger(__name__)

# Download embedding model
embedding_path = models_path / "embedding"
logger.info(f"Downloading embedding: {settings.LOCAL_HF_EMBEDDING_MODEL_NAME}")
snapshot_download(
    repo_id=settings.LOCAL_HF_EMBEDDING_MODEL_NAME,
    cache_dir=models_cache_path,
    local_dir=embedding_path,
)
logger.info("Embedding model downloaded")

# Download LLM model
logger.info(f"Downloading LLM: {settings.LOCAL_HF_LLM_MODEL_FILE}")
hf_hub_download(
    repo_id=settings.LOCAL_HF_LLM_REPO_ID,
    filename=settings.LOCAL_HF_LLM_MODEL_FILE,
    cache_dir=models_cache_path,
    local_dir=models_path,
)
logger.info("LLM model downloaded")

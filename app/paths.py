from pathlib import Path

from app._config import settings
from app.enums import PROJECT_ROOT_PATH


def _absolute_or_from_project_root(path: str) -> Path:
    if path.startswith("/"):
        return Path(path)
    return PROJECT_ROOT_PATH / path


local_data_path: Path = _absolute_or_from_project_root(settings.LOCAL_DATA_FOLDER)
models_path: Path = PROJECT_ROOT_PATH / "models"
models_cache_path: Path = models_path / "cache"

"""Utility helpers for handling file upload storage."""

from functools import lru_cache
from pathlib import Path
from typing import Union
import os

_CONTAINER_APP_ROOT = Path("/app")
_DOCKER_MEDIA_ROOT = Path("/var/app/media")


@lru_cache(maxsize=1)
def get_upload_root(path_like: Union[str, Path]) -> Path:
    """Resolve and ensure an accessible upload root directory within the container.

    Args:
        path_like: Raw path value from configuration, can be absolute or relative.

    Returns:
        Path guaranteed to exist and be writable by the application user.
    """
    # Docker 환경에서 /var/app/media가 마운트되어 있으면 사용
    if _DOCKER_MEDIA_ROOT.exists() and os.access(_DOCKER_MEDIA_ROOT, os.W_OK):
        candidate = _DOCKER_MEDIA_ROOT
        candidate.mkdir(parents=True, exist_ok=True)
        return candidate
    
    raw_path = Path(path_like)
    candidate = raw_path if raw_path.is_absolute() else (_CONTAINER_APP_ROOT / raw_path)

    try:
        candidate.mkdir(parents=True, exist_ok=True)
        return candidate
    except PermissionError:
        # Fall back to a directory scoped under /app to avoid permission issues.
        relative = (
            Path(*raw_path.parts[1:]) if raw_path.is_absolute() else raw_path
        )
        fallback = _CONTAINER_APP_ROOT / relative
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback


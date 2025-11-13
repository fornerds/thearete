"""Factory helpers for storage backend selection."""

from __future__ import annotations

from functools import lru_cache

from app.config import settings
from app.core.storage.base import BaseStorage
from app.core.storage.local import LocalStorage


@lru_cache(maxsize=1)
def get_storage() -> BaseStorage:
    """Return the configured storage backend.

    Currently supports only the local filesystem, but structured for future cloud backends.
    """
    backend = settings.upload_backend.lower() if hasattr(settings, "upload_backend") else "local"
    if backend == "local":
        return LocalStorage()
    raise ValueError(f"Unsupported upload backend: {backend}")


"""Storage backend abstractions."""

from .base import BaseStorage, StoredFile
from .factory import get_storage

__all__ = ["BaseStorage", "StoredFile", "get_storage"]


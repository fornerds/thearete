"""Base storage backend definitions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from fastapi import UploadFile


@dataclass(slots=True)
class StoredFile:
    """Metadata describing a stored file."""

    storage_path: str
    public_url: str
    content_type: str | None = None
    size: int | None = None
    thumbnail_storage_path: str | None = None
    thumbnail_url: str | None = None
    thumbnail_size: int | None = None


class BaseStorage(Protocol):
    """Interface that all storage backends must implement."""

    async def save(self, file: UploadFile, *, suffix: str | None = None) -> StoredFile:
        """Persist an uploaded file and return metadata about the stored file."""

    async def delete(self, storage_path: str) -> None:
        """Delete a file previously stored at the given storage path."""


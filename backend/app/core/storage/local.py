"""Local filesystem storage backend."""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.config import settings
from app.core.storage.base import BaseStorage, StoredFile
from app.core.uploads import get_upload_root

_DEFAULT_CHUNK_SIZE = 1024 * 1024


class LocalStorage(BaseStorage):
    """Store uploaded files on the local filesystem."""

    def __init__(self, *, root_dir: Path | None = None, url_prefix: str | None = None) -> None:
        self._upload_root = root_dir or get_upload_root(settings.upload_root)
        self._url_prefix = (url_prefix or settings.upload_url_prefix).rstrip("/")

    async def save(self, file: UploadFile, *, suffix: str | None = None) -> StoredFile:
        suffix = suffix or Path(file.filename or "").suffix
        unique_name = f"{uuid4().hex}{suffix}"
        destination = self._upload_root / "images" / unique_name
        destination.parent.mkdir(parents=True, exist_ok=True)

        total_bytes = 0
        with destination.open("wb") as buffer:
            while True:
                chunk = await file.read(_DEFAULT_CHUNK_SIZE)
                if not chunk:
                    break
                total_bytes += len(chunk)
                buffer.write(chunk)

        await file.close()

        storage_path = destination.relative_to(self._upload_root).as_posix()
        public_url = self._format_public_url(storage_path)
        return StoredFile(
            storage_path=storage_path,
            public_url=public_url,
            content_type=file.content_type,
            size=total_bytes,
        )

    async def delete(self, storage_path: str) -> None:
        target = self._upload_root / storage_path
        if target.exists():
            target.unlink()

    def _format_public_url(self, storage_path: str) -> str:
        if not self._url_prefix.startswith("/"):
            prefix = f"/{self._url_prefix}"
        else:
            prefix = self._url_prefix
        return f"{prefix}/{storage_path}"


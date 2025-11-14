"""Local filesystem storage backend."""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from PIL import Image, UnidentifiedImageError

from app.config import settings
from app.core.storage.base import BaseStorage, StoredFile
from app.core.uploads import get_upload_root

_DEFAULT_CHUNK_SIZE = 1024 * 1024
_THUMBNAIL_WIDTH = 100
_RESAMPLING_FILTER = getattr(Image, "Resampling", Image).LANCZOS


class LocalStorage(BaseStorage):
    """Store uploaded files on the local filesystem."""

    def __init__(self, *, root_dir: Path | None = None, url_prefix: str | None = None) -> None:
        self._upload_root = root_dir or get_upload_root(settings.upload_root)
        self._url_prefix = (url_prefix or settings.upload_url_prefix).rstrip("/")

    async def save(self, file: UploadFile, *, suffix: str | None = None) -> StoredFile:
        suffix = suffix or Path(file.filename or "").suffix or ".jpg"
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

        thumbnail_meta = self._create_thumbnail(destination, suffix=suffix)

        storage_path = destination.relative_to(self._upload_root).as_posix()
        public_url = self._format_public_url(storage_path)
        return StoredFile(
            storage_path=storage_path,
            public_url=public_url,
            content_type=file.content_type,
            size=total_bytes,
            thumbnail_storage_path=thumbnail_meta.get("storage_path"),
            thumbnail_url=thumbnail_meta.get("public_url"),
            thumbnail_size=thumbnail_meta.get("size"),
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

    def _create_thumbnail(self, source: Path, *, suffix: str) -> dict[str, str | int | None]:
        """Create a thumbnail image stored in the same root and return metadata."""
        try:
            with Image.open(source) as image:
                image.load()
                width, height = image.size
                if width == 0 or height == 0:
                    return {"storage_path": None, "public_url": None, "size": None}

                target_width = min(_THUMBNAIL_WIDTH, width)
                if width <= target_width:
                    thumb = image.copy()
                else:
                    ratio = target_width / float(width)
                    target_height = max(1, int(height * ratio))
                    thumb = image.resize(
                        (target_width, target_height),
                        _RESAMPLING_FILTER,
                    )

                if (suffix or "").lower() in (".jpg", ".jpeg") and thumb.mode != "RGB":
                    thumb = thumb.convert("RGB")

                thumbnail_name = f"{source.stem}_thumb{suffix}"
                destination = self._upload_root / "images" / "thumbnails" / thumbnail_name
                destination.parent.mkdir(parents=True, exist_ok=True)

                save_kwargs: dict[str, int | bool] = {}
                if (suffix or "").lower() in (".jpg", ".jpeg"):
                    save_kwargs.update({"quality": 85, "optimize": True})
                    format_ = "JPEG"
                    if thumb.mode == "RGBA":
                        thumb = thumb.convert("RGB")
                elif (suffix or "").lower() == ".png":
                    save_kwargs.update({"optimize": True})
                    format_ = "PNG"
                else:
                    format_ = image.format or "PNG"

                thumb.save(destination, format=format_, **save_kwargs)
                storage_path = destination.relative_to(self._upload_root).as_posix()
                return {
                    "storage_path": storage_path,
                    "public_url": self._format_public_url(storage_path),
                    "size": destination.stat().st_size,
                }
        except (UnidentifiedImageError, OSError):
            return {"storage_path": None, "public_url": None, "size": None}



"""Service layer for image uploads."""

from __future__ import annotations

from typing import Sequence

from fastapi import UploadFile

from app.core.storage import StoredFile, get_storage
from app.db.repositories.uploaded_image_repo import UploadedImageRepository
from sqlalchemy.ext.asyncio import AsyncSession


class UploadService:
    """Handle image uploads and persistence of their metadata."""

    def __init__(self) -> None:
        self._storage = get_storage()
        self._repository = UploadedImageRepository()

    async def upload_images(
        self,
        db: AsyncSession,
        files: Sequence[UploadFile],
    ):
        stored_records = []
        stored_files: list[StoredFile] = []
        try:
            for upload in files:
                stored = await self._storage.save(upload)
                stored_files.append(stored)
                payload = {
                    "original_filename": upload.filename,
                    "storage_path": stored.storage_path,
                    "public_url": stored.public_url,
                    "content_type": stored.content_type,
                    "file_size": stored.size,
                    "storage_backend": type(self._storage).__name__.replace("Storage", "").lower(),
                }
                record = await self._repository.create(db, payload)
                stored_records.append(record)
            return stored_records
        except Exception:
            for stored in stored_files:
                await self._storage.delete(stored.storage_path)
            raise


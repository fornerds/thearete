"""Service layer for treatment photos domain."""

from typing import Any, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.storage import get_storage
from app.db.models.treatment_session_image import TreatmentSessionImage
from app.db.repositories.treatment_session_image_repo import TreatmentSessionImageRepository
from app.db.repositories.uploaded_image_repo import UploadedImageRepository
from app.services.treatment_sessions_service import TreatmentSessionsService


class TreatmentPhotosService:
    """Service for treatment photos domain operations (session image mappings)."""

    def __init__(self) -> None:
        self.treatment_sessions_service = TreatmentSessionsService()
        self.session_image_repository = TreatmentSessionImageRepository()
        self.uploaded_image_repository = UploadedImageRepository()

    async def attach_treatment_photos(
        self,
        db: AsyncSession,
        *,
        treatment_id: int,
        session_id: int,
        images: List[Dict[str, Any]],
        shop_id: int,
    ) -> List[TreatmentSessionImage]:
        """Attach uploaded images to a treatment session."""
        session = await self.treatment_sessions_service.get_treatment_session_by_id(
            db,
            session_id,
            shop_id=shop_id,
        )
        if not session:
            raise ValueError("해당 시술 회차를 찾을 수 없습니다.")

        await self.treatment_sessions_service.set_session_images(
            db,
            treatment_id=treatment_id,
            session_id=session_id,
            images_payload=images,
        )
        return await self.session_image_repository.get_by_session(
            db,
            session_id=session_id,
        )

    async def list_treatment_photos(
        self,
        db: AsyncSession,
        *,
        treatment_id: Optional[int] = None,
        session_id: Optional[int] = None,
        shop_id: Optional[int] = None,
    ) -> List[TreatmentSessionImage]:
        """List treatment session image mappings."""
        return await self.session_image_repository.list_mappings(
            db,
            treatment_id=treatment_id,
            session_id=session_id,
            shop_id=shop_id,
        )

    async def delete_treatment_photo(
        self,
        db: AsyncSession,
        mapping_id: int,
        *,
        shop_id: int,
    ) -> bool:
        """Remove an image mapping from a treatment session and cleanup if orphaned."""
        target = await self.session_image_repository.get_by_id(
            db,
            mapping_id,
            shop_id=shop_id,
        )
        if not target:
            return False

        uploaded_image = target.uploaded_image
        await db.delete(target)
        await db.commit()

        if uploaded_image:
            remaining = await self.session_image_repository.get_by_image_ids(
                db,
                image_ids=[uploaded_image.id],
            )
            if not remaining:
                storage = get_storage()
                await storage.delete(uploaded_image.storage_path)
                await self.uploaded_image_repository.mark_deleted(
                    db,
                    [uploaded_image.id],
                )
        return True
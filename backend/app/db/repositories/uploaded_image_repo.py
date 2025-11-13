"""Repository for uploaded image metadata."""

from typing import Iterable, Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.uploaded_image import UploadedImage
from app.db.models.treatment_session_image import TreatmentSessionImage
from app.db.models.customer import Customer
from app.db.models.treatment import Treatment
from app.db.models.treatment_session import TreatmentSession
from sqlalchemy import or_


class UploadedImageRepository:
    """CRUD helpers for `UploadedImage` records."""

    async def create(self, db: AsyncSession, data: dict) -> UploadedImage:
        image = UploadedImage(**data)
        db.add(image)
        await db.commit()
        await db.refresh(image)
        return image

    async def mark_deleted(self, db: AsyncSession, image_ids: Iterable[int]) -> None:
        ids = tuple(image_ids)
        if not ids:
            return
        stmt = update(UploadedImage).where(UploadedImage.id.in_(ids)).values(is_deleted=True)
        await db.execute(stmt)
        await db.commit()

    async def get_by_ids(self, db: AsyncSession, image_ids: Sequence[int]) -> list[UploadedImage]:
        if not image_ids:
            return []
        stmt = select(UploadedImage).where(UploadedImage.id.in_(image_ids))
        result = await db.execute(stmt)
        return list(result.scalars())

    async def get_by_urls(
        self,
        db: AsyncSession,
        *,
        urls: Sequence[str],
    ) -> list[UploadedImage]:
        if not urls:
            return []
        stmt = select(UploadedImage).where(UploadedImage.public_url.in_(urls)).where(
            UploadedImage.is_deleted == False  # noqa: E712
        )
        result = await db.execute(stmt)
        return list(result.scalars())

    async def get_unlinked_images(
        self,
        db: AsyncSession,
        image_ids: Iterable[int] | None = None,
    ) -> list[UploadedImage]:
        stmt = (
            select(UploadedImage)
            .outerjoin(
                TreatmentSessionImage,
                TreatmentSessionImage.uploaded_image_id == UploadedImage.id,
            )
            .where(UploadedImage.is_deleted == False)  # noqa: E712
            .where(TreatmentSessionImage.id.is_(None))
        )
        if image_ids:
            stmt = stmt.where(UploadedImage.id.in_(tuple(image_ids)))
        result = await db.execute(stmt)
        return list(result.scalars())

    async def get_by_id_with_shop_check(
        self,
        db: AsyncSession,
        image_id: int,
        shop_id: int,
    ) -> UploadedImage | None:
        """Get uploaded image by ID and verify shop access through treatment session."""

        stmt = (
            select(UploadedImage)
            .join(
                TreatmentSessionImage,
                TreatmentSessionImage.uploaded_image_id == UploadedImage.id,
            )
            .join(
                TreatmentSession,
                TreatmentSessionImage.session_id == TreatmentSession.id,
            )
            .join(
                Treatment,
                TreatmentSession.treatment_id == Treatment.id,
            )
            .join(
                Customer,
                Treatment.customer_id == Customer.id,
            )
            .where(UploadedImage.id == image_id)
            .where(UploadedImage.is_deleted == False)  # noqa: E712
            .where(Customer.shop_id == shop_id)
            .where(or_(TreatmentSession.is_deleted == False, TreatmentSession.is_deleted.is_(None)))  # noqa: E712
            .where(or_(Treatment.is_deleted == False, Treatment.is_deleted.is_(None)))  # noqa: E712
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_url_with_shop_check(
        self,
        db: AsyncSession,
        url: str,
        shop_id: int,
    ) -> UploadedImage | None:
        """Get uploaded image by URL and verify shop access through treatment session.
        
        First tries to find image linked to treatment session (with shop check).
        If not found, tries to find unlinked image (no shop check - TODO: add shop_id to uploaded_image).
        """
        # First, try to find image linked to treatment session (with shop check)
        stmt = (
            select(UploadedImage)
            .join(
                TreatmentSessionImage,
                TreatmentSessionImage.uploaded_image_id == UploadedImage.id,
            )
            .join(
                TreatmentSession,
                TreatmentSessionImage.session_id == TreatmentSession.id,
            )
            .join(
                Treatment,
                TreatmentSession.treatment_id == Treatment.id,
            )
            .join(
                Customer,
                Treatment.customer_id == Customer.id,
            )
            .where(UploadedImage.public_url == url)
            .where(UploadedImage.is_deleted == False)  # noqa: E712
            .where(Customer.shop_id == shop_id)
            .where(or_(TreatmentSession.is_deleted == False, TreatmentSession.is_deleted.is_(None)))  # noqa: E712
            .where(or_(Treatment.is_deleted == False, Treatment.is_deleted.is_(None)))  # noqa: E712
        )
        result = await db.execute(stmt)
        image = result.scalar_one_or_none()
        
        # If not found in treatment session, try to find unlinked image
        # TODO: Add shop_id to uploaded_image table for proper shop check
        if image is None:
            stmt = (
                select(UploadedImage)
                .outerjoin(
                    TreatmentSessionImage,
                    TreatmentSessionImage.uploaded_image_id == UploadedImage.id,
                )
                .where(UploadedImage.public_url == url)
                .where(UploadedImage.is_deleted == False)  # noqa: E712
                .where(TreatmentSessionImage.id.is_(None))  # Only unlinked images
            )
            result = await db.execute(stmt)
            image = result.scalar_one_or_none()
        
        return image


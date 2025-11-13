"""Repository for treatment session image mappings."""

from typing import Iterable, Optional, Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.treatment_session_image import TreatmentSessionImage


class TreatmentSessionImageRepository:
    """CRUD helpers for treatment session image associations."""

    async def replace_mappings(
        self,
        db: AsyncSession,
        *,
        session_id: int,
        mappings: Sequence[dict],
    ) -> list[TreatmentSessionImage]:
        await db.execute(
            delete(TreatmentSessionImage).where(
                TreatmentSessionImage.session_id == session_id
            )
        )
        created: list[TreatmentSessionImage] = []
        for payload in mappings:
            mapping = TreatmentSessionImage(**payload)
            db.add(mapping)
            created.append(mapping)
        await db.commit()
        for mapping in created:
            await db.refresh(mapping)
        return created

    async def get_by_session(
        self,
        db: AsyncSession,
        *,
        session_id: int,
    ) -> list[TreatmentSessionImage]:
        stmt = (
            select(TreatmentSessionImage)
            .options(selectinload(TreatmentSessionImage.uploaded_image))
            .where(TreatmentSessionImage.session_id == session_id)
        )
        result = await db.execute(stmt)
        return list(result.scalars())

    async def get_by_image_ids(
        self,
        db: AsyncSession,
        *,
        image_ids: Iterable[int],
    ) -> list[TreatmentSessionImage]:
        ids = tuple(image_ids)
        if not ids:
            return []
        stmt = select(TreatmentSessionImage).where(
            TreatmentSessionImage.uploaded_image_id.in_(ids)
        )
        result = await db.execute(stmt)
        return list(result.scalars())

    async def get_by_id(
        self,
        db: AsyncSession,
        mapping_id: int,
        *,
        shop_id: int | None = None,
    ) -> Optional[TreatmentSessionImage]:
        from app.db.models.customer import Customer
        from app.db.models.treatment import Treatment
        from app.db.models.treatment_session import TreatmentSession
        from sqlalchemy import or_

        stmt = (
            select(TreatmentSessionImage)
            .options(selectinload(TreatmentSessionImage.uploaded_image))
            .join(TreatmentSession, TreatmentSessionImage.session_id == TreatmentSession.id)
            .join(Treatment, TreatmentSession.treatment_id == Treatment.id)
            .join(Customer, Treatment.customer_id == Customer.id)
            .where(TreatmentSessionImage.id == mapping_id)
        )
        if shop_id is not None:
            stmt = stmt.where(Customer.shop_id == shop_id)
        stmt = stmt.where(or_(TreatmentSession.is_deleted == False, TreatmentSession.is_deleted.is_(None)))  # noqa: E712
        stmt = stmt.where(or_(Treatment.is_deleted == False, Treatment.is_deleted.is_(None)))  # noqa: E712
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_mappings(
        self,
        db: AsyncSession,
        *,
        treatment_id: int | None = None,
        session_id: int | None = None,
        shop_id: int | None = None,
    ) -> list[TreatmentSessionImage]:
        from app.db.models.customer import Customer
        from app.db.models.treatment import Treatment
        from app.db.models.treatment_session import TreatmentSession
        from sqlalchemy import or_

        stmt = (
            select(TreatmentSessionImage)
            .options(selectinload(TreatmentSessionImage.uploaded_image))
            .join(TreatmentSession, TreatmentSessionImage.session_id == TreatmentSession.id)
            .join(Treatment, TreatmentSession.treatment_id == Treatment.id)
            .join(Customer, Treatment.customer_id == Customer.id)
            .where(or_(TreatmentSession.is_deleted == False, TreatmentSession.is_deleted.is_(None)))  # noqa: E712
            .where(or_(Treatment.is_deleted == False, Treatment.is_deleted.is_(None)))  # noqa: E712
        )

        if treatment_id is not None:
            stmt = stmt.where(TreatmentSessionImage.treatment_id == treatment_id)
        if session_id is not None:
            stmt = stmt.where(TreatmentSessionImage.session_id == session_id)
        if shop_id is not None:
            stmt = stmt.where(Customer.shop_id == shop_id)

        result = await db.execute(stmt)
        return list(result.scalars())


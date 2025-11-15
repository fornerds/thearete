"""Service layer for treatment sessions domain."""

from typing import Any, Dict, Iterable, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.treatment_session import TreatmentSession
from app.db.repositories.treatment_session_image_repo import TreatmentSessionImageRepository
from app.db.repositories.treatment_sessions_repo import TreatmentSessionsRepository
from app.db.repositories.uploaded_image_repo import UploadedImageRepository


class TreatmentSessionsService:
    """Service for treatment sessions domain operations."""

    def __init__(self) -> None:
        self.repository = TreatmentSessionsRepository()
        self.session_image_repository = TreatmentSessionImageRepository()
        self.uploaded_image_repository = UploadedImageRepository()

    async def create_treatment_session(
        self,
        db: AsyncSession,
        request_data: Dict[str, Any],
        shop_id: Optional[int] = None,
    ) -> TreatmentSession:
        """Create new treatment session."""
        images_payload = request_data.pop("images", [])
        treatment_id = request_data.get("treatment_id")
        
        if shop_id:
            from app.core.exceptions import ForbiddenException
            from app.db.models.customer import Customer
            from app.db.models.treatment import Treatment
            from sqlalchemy import or_, select

            if treatment_id:
                result = await db.execute(
                    select(Treatment)
                    .join(Customer)
                    .where(Treatment.id == treatment_id)
                    .where(or_(Treatment.is_deleted == False, Treatment.is_deleted.is_(None)))  # noqa: E712
                    .where(Customer.shop_id == shop_id)
                )
                treatment = result.scalar_one_or_none()
                if not treatment:
                    raise ForbiddenException("Treatment not found or does not belong to your shop")

        # Calculate sequence: count existing sessions for this treatment + 1
        if treatment_id:
            from app.db.models.treatment_session import TreatmentSession
            from sqlalchemy import select, func, or_
            
            result = await db.execute(
                select(func.count(TreatmentSession.id))
                .where(TreatmentSession.treatment_id == treatment_id)
                .where(or_(TreatmentSession.is_deleted == False, TreatmentSession.is_deleted.is_(None)))
            )
            existing_count = result.scalar() or 0
            request_data["sequence"] = existing_count + 1
        else:
            # If treatment_id is not provided, default to 1 (should not happen in normal flow)
            request_data["sequence"] = 1

        session = await self.repository.create(db, request_data)
        if images_payload:
            await self.set_session_images(
                db,
                treatment_id=session.treatment_id,
                session_id=session.id,
                images_payload=images_payload,
            )
            session = await self.repository.get_by_id(db, session.id, shop_id=shop_id)
        return session

    async def list_treatment_sessions(
        self,
        db: AsyncSession,
        treatment_id: Optional[int] = None,
        shop_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[TreatmentSession]:
        """List all treatment sessions."""
        return await self.repository.get_all(
            db,
            treatment_id=treatment_id,
            shop_id=shop_id,
            skip=skip,
            limit=limit,
        )

    async def get_treatment_session_by_id(
        self,
        db: AsyncSession,
        session_id: int,
        shop_id: Optional[int] = None,
    ) -> Optional[TreatmentSession]:
        """Get treatment session by ID."""
        return await self.repository.get_by_id(db, session_id, shop_id=shop_id)

    async def update_treatment_session(
        self,
        db: AsyncSession,
        session_id: int,
        request_data: Dict[str, Any],
        shop_id: Optional[int] = None,
    ) -> Optional[TreatmentSession]:
        """Update treatment session by ID."""
        images_payload = request_data.pop("images", None)
        if shop_id:
            session = await self.get_treatment_session_by_id(db, session_id, shop_id=shop_id)
            if not session:
                return None
        result = await self.repository.update(db, session_id, request_data)
        if result and images_payload is not None:
            await self.set_session_images(
                db,
                treatment_id=result.treatment_id,
                session_id=result.id,
                images_payload=images_payload,
            )
            result = await self.repository.get_by_id(db, result.id, shop_id=shop_id)
        return result

    async def delete_treatment_session(
        self,
        db: AsyncSession,
        session_id: int,
        shop_id: Optional[int] = None,
    ) -> bool:
        """Delete treatment session by ID."""
        if shop_id:
            session = await self.get_treatment_session_by_id(db, session_id, shop_id=shop_id)
            if not session:
                return False
        return await self.repository.delete(db, session_id)

    async def set_session_images(
        self,
        db: AsyncSession,
        *,
        treatment_id: int,
        session_id: int,
        images_payload: List[Dict[str, Any]],
    ) -> None:
        existing_mappings = await self.session_image_repository.get_by_session(
            db,
            session_id=session_id,
        )
        # 기존에 등록된 이미지 URL 목록 생성 (URL -> mapping 매핑)
        existing_url_to_mapping = {
            mapping.uploaded_image.public_url: mapping
            for mapping in existing_mappings 
            if mapping.uploaded_image
        }
        existing_urls = set(existing_url_to_mapping.keys())

        # remove=true인 이미지 처리
        images_to_remove = [
            item for item in images_payload 
            if item.get("remove") is True and item.get("url")
        ]
        
        if images_to_remove:
            await self._remove_session_images(
                db,
                session_id=session_id,
                urls_to_remove=[item["url"] for item in images_to_remove],
                existing_url_to_mapping=existing_url_to_mapping,
            )

        if not images_payload:
            # images_payload가 비어있으면 기존 이미지 유지 (삭제하지 않음)
            return

        # remove가 아닌 이미지들만 처리
        images_to_add = [
            item for item in images_payload 
            if item.get("remove") is not True
        ]

        if not images_to_add:
            return

        urls = [item["url"] for item in images_to_add if item.get("url")]
        uploaded_images = await self.uploaded_image_repository.get_by_urls(
            db,
            urls=urls,
        )
        url_to_image = {image.public_url: image for image in uploaded_images}
        missing_urls = [url for url in urls if url not in url_to_image]
        if missing_urls:
            raise ValueError(f"다음 이미지가 존재하지 않거나 권한이 없습니다: {', '.join(missing_urls)}")

        # 중복되지 않는 새로운 이미지만 필터링
        new_mappings = []
        
        for payload in images_to_add:
            url = payload.get("url")
            if not url:
                continue
            
            # 기존에 등록된 이미지 URL과 중복되는 경우 건너뛰기
            if url in existing_urls:
                continue
            
            image = url_to_image[url]
            new_mappings.append(
                {
                    "treatment_id": treatment_id,
                    "session_id": session_id,
                    "uploaded_image_id": image.id,
                    "photo_type": payload.get("type"),
                }
            )

        # 새로운 매핑만 추가 (기존 매핑은 유지)
        if new_mappings:
            await self.session_image_repository.add_mappings(
                db,
                session_id=session_id,
                mappings=new_mappings,
            )

    async def _remove_session_images(
        self,
        db: AsyncSession,
        *,
        session_id: int,
        urls_to_remove: List[str],
        existing_url_to_mapping: Dict[str, Any],
    ) -> None:
        """Remove session images by URLs."""
        from sqlalchemy import delete
        from app.db.models.treatment_session_image import TreatmentSessionImage
        from app.core.storage import get_storage

        mappings_to_remove = []
        image_ids_to_remove = []
        
        for url in urls_to_remove:
            if url in existing_url_to_mapping:
                mapping = existing_url_to_mapping[url]
                mappings_to_remove.append(mapping.id)
                if mapping.uploaded_image:
                    image_ids_to_remove.append(mapping.uploaded_image_id)

        if not mappings_to_remove:
            return

        # 세션 이미지 매핑 삭제
        await db.execute(
            delete(TreatmentSessionImage).where(
                TreatmentSessionImage.id.in_(mappings_to_remove)
            )
        )
        await db.commit()

        # 업로드된 이미지와 실제 파일 삭제 (hard delete)
        if image_ids_to_remove:
            images = await self.uploaded_image_repository.get_by_ids(
                db,
                image_ids_to_remove,
            )
            
            storage = get_storage()
            for image in images:
                # 실제 파일 삭제
                if image.storage_path:
                    try:
                        await storage.delete(image.storage_path)
                    except Exception:
                        pass  # 파일이 이미 없을 수 있음
                if image.thumbnail_storage_path:
                    try:
                        await storage.delete(image.thumbnail_storage_path)
                    except Exception:
                        pass  # 파일이 이미 없을 수 있음
            
            # 업로드된 이미지 hard delete
            from app.db.models.uploaded_image import UploadedImage
            await db.execute(
                delete(UploadedImage).where(
                    UploadedImage.id.in_(image_ids_to_remove)
                )
            )
            await db.commit()

    async def _cleanup_orphan_images(
        self,
        db: AsyncSession,
        *,
        candidate_image_ids: Optional[Iterable[int]],
    ) -> None:
        if not candidate_image_ids:
            return

        orphan_images = await self.uploaded_image_repository.get_unlinked_images(
            db,
            image_ids=candidate_image_ids,
        )
        if not orphan_images:
            return

        from app.core.storage import get_storage

        storage = get_storage()
        for image in orphan_images:
            await storage.delete(image.storage_path)
            if image.thumbnail_storage_path:
                await storage.delete(image.thumbnail_storage_path)
        await self.uploaded_image_repository.mark_deleted(
            db,
            [image.id for image in orphan_images],
        )

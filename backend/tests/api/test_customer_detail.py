"""Tests for customer detail endpoint focusing on treatment ordering."""

from datetime import datetime, timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.v1 import routes_customer
from app.core.auth import get_current_shop
from app.db.session import get_db
from app.main import app


def _iso(dt: datetime) -> str:
    return dt.isoformat()


class FakeImage:
    def __init__(self, sequence_no: int, photo_type: str, created_at: datetime, updated_at: datetime):
        self.sequence_no = sequence_no
        self.photo_type = photo_type
        self.created_at = created_at
        self.updated_at = updated_at
        self.uploaded_image = SimpleNamespace(
            id=sequence_no,
            public_url=f"https://example.com/{sequence_no}",
            thumbnail_url=f"https://example.com/{sequence_no}_thumb",
        )


class FakeSession:
    def __init__(self, session_id: int, base_time: datetime, image_offset: int):
        self.id = session_id
        self.treatment_date = base_time.date()
        self.duration_minutes = 30
        self.is_completed = False
        self.is_deleted = False
        self.created_at = base_time
        self.updated_at = base_time + timedelta(hours=1)
        image_time = base_time + timedelta(hours=image_offset)
        self.images = [
            FakeImage(sequence_no=session_id, photo_type="BEFORE", created_at=image_time, updated_at=image_time)
        ]


class FakeTreatment:
    def __init__(self, treatment_id: int, base_time: datetime, extra_offset: int):
        self.id = treatment_id
        self.type = f"type-{treatment_id}"
        self.area = f"area-{treatment_id}"
        self.is_completed = False
        self.is_deleted = False
        self.created_at = base_time
        self.updated_at = base_time + timedelta(minutes=10)
        session_time = base_time + timedelta(days=extra_offset)
        self.treatment_session = [
            FakeSession(session_id=treatment_id * 10, base_time=session_time, image_offset=extra_offset)
        ]


class FakeCustomer:
    def __init__(self):
        now = datetime(2024, 1, 1, 10, 0, 0)
        later = datetime(2024, 1, 2, 12, 0, 0)
        self.id = 1
        self.shop_id = 1
        self.name = "Test Customer"
        self.gender = "F"
        self.age = 30
        self.skin_type = "dry"
        self.marked = 1
        self.created_at = now
        self.updated_at = later
        self.treatment = [
            FakeTreatment(1, now, extra_offset=1),
            FakeTreatment(2, later, extra_offset=2),
        ]


class FakeCustomerService:
    def __init__(self, *args, **kwargs):
        self.customer = FakeCustomer()

    async def get_customer_by_id(self, db, customer_id: int):
        return self.customer if customer_id == self.customer.id else None


@pytest.mark.asyncio
async def test_customer_detail_treatments_sorted_and_latest_time(monkeypatch):
    """Ensure treatments are sorted by latest update time and expose the timestamp."""

    fake_service = FakeCustomerService()
    monkeypatch.setattr(routes_customer, "CustomerService", lambda: fake_service)

    fake_shop = SimpleNamespace(id=1)

    async def override_get_current_shop():
        return fake_shop

    async def override_get_db():
        yield AsyncMock()

    previous_overrides = dict(app.dependency_overrides)
    app.dependency_overrides[get_current_shop] = override_get_current_shop
    app.dependency_overrides[get_db] = override_get_db

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/customers/1")
    finally:
        app.dependency_overrides = previous_overrides

    assert response.status_code == 200
    payload = response.json()
    treatments = payload["treatments"]

    assert len(treatments) == 2

    assert treatments[0]["created_at"] is not None
    assert treatments[1]["created_at"] is not None

    first_latest = datetime.fromisoformat(treatments[0]["latest_update_time"])
    second_latest = datetime.fromisoformat(treatments[1]["latest_update_time"])
    assert first_latest >= second_latest

    customer_latest = datetime.fromisoformat(payload["latest_update_time"])
    assert customer_latest == first_latest


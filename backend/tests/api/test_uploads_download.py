"""Tests for image download endpoint, including thumbnail access."""

from types import SimpleNamespace

import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock

from app.main import app
from app.api.v1 import routes_uploads
from app.core.auth import get_current_shop
from app.db.session import get_db


@pytest.mark.asyncio
async def test_download_thumbnail_path(monkeypatch):
    """Ensure thumbnail paths are resolved via the download endpoint."""

    image_path = "images/thumbnails/63eee1c647f04706808d41dffaf38bcd_thumb.png"
    upload_prefix = routes_uploads.settings.upload_url_prefix.rstrip("/")
    if not upload_prefix.startswith("/"):
        upload_prefix = f"/{upload_prefix}"
    expected_url = f"{upload_prefix}/{image_path}"

    fake_shop = SimpleNamespace(id=123)
    fake_image = SimpleNamespace(
        storage_path=image_path,
        content_type="image/png",
    )

    async def override_get_current_shop():
        return fake_shop

    async def override_get_db():
        yield AsyncMock()  # Placeholder session, not used due to mocking

    async def mock_get_by_url(self, db, url, shop_id):
        assert url == expected_url
        assert shop_id == fake_shop.id
        return fake_image

    previous_overrides = dict(app.dependency_overrides)
    app.dependency_overrides[get_current_shop] = override_get_current_shop
    app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setattr(
        routes_uploads.UploadedImageRepository,
        "get_by_url_with_shop_check",
        mock_get_by_url,
    )

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get(f"/{routes_uploads._upload_url_prefix}/{image_path}")
    finally:
        app.dependency_overrides = previous_overrides

    assert response.status_code == 200
    assert response.headers["X-Accel-Redirect"] == f"/_protected/{image_path}"
    assert response.headers["Content-Type"] == "image/png"
    assert response.headers["Cache-Control"] == "private, max-age=600"


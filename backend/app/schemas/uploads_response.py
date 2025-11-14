"""Response schemas for upload endpoints."""

from pydantic import BaseModel, Field
from typing import List, Optional


class UploadedImageItem(BaseModel):
    image_id: str = Field(..., description="업로드된 이미지 ID")
    url: str = Field(..., description="이미지 접근 URL")
    original_filename: Optional[str] = Field(None, description="원본 파일명")
    thumbnail_url: Optional[str] = Field(None, description="썸네일 이미지 접근 URL")


class UploadImagesResponse(BaseModel):
    uploads: List[UploadedImageItem]


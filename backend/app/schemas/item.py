"""Item Pydantic schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.common import BaseSchema, TimestampMixin


class ItemBase(BaseModel):
    """Base item schema."""
    
    title: str = Field(min_length=1, max_length=255, description="Item title")
    description: Optional[str] = Field(None, description="Item description")
    price: Optional[float] = Field(None, ge=0, description="Item price")


class ItemCreate(ItemBase):
    """Item creation schema."""
    
    pass


class ItemUpdate(BaseModel):
    """Item update schema."""
    
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Item title")
    description: Optional[str] = Field(None, description="Item description")
    price: Optional[float] = Field(None, ge=0, description="Item price")
    is_active: Optional[bool] = Field(None, description="Item active status")


class ItemInDB(ItemBase, TimestampMixin):
    """Item in database schema."""
    
    id: int = Field(description="Item ID")
    owner_id: int = Field(description="Owner user ID")
    is_active: bool = Field(description="Item active status")


class Item(ItemInDB):
    """Item response schema."""
    
    owner: Optional["UserProfile"] = Field(None, description="Item owner")


class ItemWithOwner(ItemInDB):
    """Item with owner details schema."""
    
    owner: "UserProfile" = Field(description="Item owner")


# Import here to avoid circular imports
from app.schemas.user import UserProfile  # noqa: E402

# Update forward references
Item.model_rebuild()
ItemWithOwner.model_rebuild()

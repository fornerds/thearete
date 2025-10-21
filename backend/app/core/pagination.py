"""Pagination utilities for API responses."""

from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar('T')


class PaginationParams(BaseModel):
    """Pagination query parameters."""
    
    page: int = Field(default=1, ge=1, description="Page number")
    size: int = Field(default=20, ge=1, le=100, description="Page size")
    
    @property
    def offset(self) -> int:
        """Calculate offset from page and size."""
        return (self.page - 1) * self.size


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response model."""
    
    items: List[T] = Field(description="List of items")
    total: int = Field(description="Total number of items")
    page: int = Field(description="Current page number")
    size: int = Field(description="Page size")
    pages: int = Field(description="Total number of pages")
    has_next: bool = Field(description="Whether there is a next page")
    has_prev: bool = Field(description="Whether there is a previous page")
    
    @classmethod
    def create(
        cls,
        items: List[T],
        total: int,
        page: int,
        size: int,
    ) -> "PaginatedResponse[T]":
        """Create a paginated response."""
        pages = (total + size - 1) // size  # Ceiling division
        
        return cls(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1,
        )


def paginate_query(query, pagination: PaginationParams):
    """Apply pagination to a SQLAlchemy query."""
    return query.offset(pagination.offset).limit(pagination.size)

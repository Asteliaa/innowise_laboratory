"""Pydantic schemas for request and response models."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    """Base fields shared by reading and creation schemas."""

    title: str
    author: str
    year: Optional[int] = None


class BookCreate(BookBase):
    """Schema for creating a new book."""


class BookUpdate(BaseModel):
    """Schema for updating book details (all fields optional)."""

    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None


class BookRead(BookBase):
    """Schema used when returning a book from the API."""

    id: int

    model_config = ConfigDict(from_attributes=True)

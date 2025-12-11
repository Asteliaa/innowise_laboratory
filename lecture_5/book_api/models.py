"""SQLAlchemy ORM models for the Book API."""

from __future__ import annotations

from sqlalchemy import Column, Integer, String

from database import Base


class Book(Base):  # pylint: disable=too-few-public-methods
    """ORM model representing a book in the collection."""

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False, index=True)
    year = Column(Integer, nullable=True, index=True)

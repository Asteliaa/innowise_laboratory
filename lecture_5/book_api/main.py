"""Simple Book Collection API using FastAPI and SQLAlchemy.

Run the app with:
    uvicorn main:app --reload
"""

from __future__ import annotations

from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

import database
import models
import schemas

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Simple Book Collection API")


@app.post(
    "/books/",
    response_model=schemas.BookRead,
    status_code=status.HTTP_201_CREATED,
    tags=["books"],
)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(database.get_db),
) -> schemas.BookRead:
    """Add a new book to the collection (POST /books/)."""
    db_book = models.Book(
        title=book.title,
        author=book.author,
        year=book.year,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@app.get(
    "/books/",
    response_model=List[schemas.BookRead],
    tags=["books"],
)
def list_books(
    skip: int = Query(
        0,
        ge=0,
        description="Number of records to skip for pagination.",
    ),
    limit: int = Query(
        10,
        gt=0,
        le=100,
        description="Maximum number of records to return.",
    ),
    db: Session = Depends(database.get_db),
) -> List[schemas.BookRead]:
    """Get all books with simple pagination (GET /books/)."""
    return (
        db.query(models.Book)
        .offset(skip)
        .limit(limit)
        .all()
    )


@app.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["books"],
)
def delete_book(
    book_id: int,
    db: Session = Depends(database.get_db),
) -> None:
    """Delete a book by ID (DELETE /books/{book_id})."""
    db_book = (
        db.query(models.Book)
        .filter(models.Book.id == book_id)
        .first()
    )
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found.",
        )

    db.delete(db_book)
    db.commit()


@app.put(
    "/books/{book_id}",
    response_model=schemas.BookRead,
    tags=["books"],
)
def update_book(
    book_id: int,
    book_update: schemas.BookUpdate,
    db: Session = Depends(database.get_db),
) -> schemas.BookRead:
    """Update book details (PUT /books/{book_id})."""
    db_book = (
        db.query(models.Book)
        .filter(models.Book.id == book_id)
        .first()
    )
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found.",
        )

    update_data = book_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_book, field, value)

    db.commit()
    db.refresh(db_book)
    return db_book


@app.get(
    "/books/search/",
    response_model=List[schemas.BookRead],
    tags=["books"],
)
def search_books(
    title: Optional[str] = Query(
        None,
        description="Search by title (substring, case-insensitive).",
    ),
    author: Optional[str] = Query(
        None,
        description="Search by author (substring, case-insensitive).",
    ),
    year: Optional[int] = Query(
        None,
        description="Search by exact publication year.",
    ),
    skip: int = Query(
        0,
        ge=0,
        description="Number of records to skip for pagination.",
    ),
    limit: int = Query(
        10,
        gt=0,
        le=100,
        description="Maximum number of records to return.",
    ),
    db: Session = Depends(database.get_db),
) -> List[schemas.BookRead]:
    """Search books by title, author, or year with pagination."""
    query = db.query(models.Book)

    if title is not None:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))
    if author is not None:
        query = query.filter(models.Book.author.ilike(f"%{author}%"))
    if year is not None:
        query = query.filter(models.Book.year == year)

    return query.offset(skip).limit(limit).all()

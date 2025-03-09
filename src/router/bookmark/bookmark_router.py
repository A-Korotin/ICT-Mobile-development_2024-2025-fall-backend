from typing import List

from fastapi import APIRouter
from fastapi.params import Depends, Security
from fastapi_jwt import JwtAccessBearer, JwtAuthorizationCredentials
from sqlalchemy import Select, delete
from sqlmodel import Session, select

from src.db.db import get_session
from src.model.bookmark import Bookmark
from src.router.bookmark.dto import BookmarkDto
from src.util.crypt import JWT_SECRET

router = APIRouter()
access_security = JwtAccessBearer(secret_key=JWT_SECRET, auto_error=True)


@router.post("/bookmarks", response_model=None, status_code=200)
def save_bookmarks(bookmarks: List[BookmarkDto], credentials: JwtAuthorizationCredentials = Security(access_security),
                   db: Session = Depends(get_session)) -> None:
    db.exec(delete(Bookmark).where(Bookmark.username == credentials['username']))

    for bookmark in bookmarks:
        bookmark_entry = Bookmark(**bookmark.model_dump(), username=credentials['username'])
        db.add(bookmark_entry)

    db.commit()

@router.get("/bookmarks", response_model=List[BookmarkDto])
def get_bookmarks(book_id: int, credentials: JwtAuthorizationCredentials = Security(access_security), db: Session = Depends(get_session)):
    bookmarks = db.exec(select(Bookmark).where(Bookmark.book_id == book_id and Bookmark.username == credentials['username'])).all()

    return bookmarks

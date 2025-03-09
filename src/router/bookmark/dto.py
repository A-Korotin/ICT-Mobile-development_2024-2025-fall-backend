from pydantic import BaseModel


class BookmarkDto(BaseModel):
    id: int
    book_id: int
    start: int
    end: int
    color: int
    fragment: str


class BookmarkReturnDto(BaseModel):
    id: int
    book_id: int
    start: int
    end: int
    color: int
    fragment: str
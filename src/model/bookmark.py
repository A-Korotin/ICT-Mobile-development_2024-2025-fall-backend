from sqlmodel import SQLModel, Field


class Bookmark(SQLModel, table=True):
    id: int = Field(primary_key=True)
    book_id: int = Field()
    username: str = Field(foreign_key="user.username")
    start: int = Field()
    end: int = Field()
    color: int = Field()
    fragment: str = Field()
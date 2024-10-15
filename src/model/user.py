from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    username: str = Field(primary_key=True)
    password: str
    name: str = Field()
    profile_picture: str = Field()
    is_active: bool = Field(default=True)

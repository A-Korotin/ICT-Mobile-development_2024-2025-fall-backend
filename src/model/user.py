from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    username: str = Field(primary_key=True)
    password: str
    name: str = Field(default='')
    profile_picture: str = Field(default='')
    is_active: bool = Field(default=True)

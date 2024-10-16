from pydantic import BaseModel, Field
from typing import Optional


class RegisterDto(BaseModel):
    username: str = Field(max_length=50, min_length=4)
    password: str = Field(max_length=255, min_length=6)


class LoginDto(BaseModel):
    username: str = Field(max_length=50, min_length=4)
    password: str = Field(max_length=255, min_length=6)


class JwtDto(BaseModel):
    token: str


class AccountInfoEditDto(BaseModel):
    name: Optional[str] = None
    profile_picture: Optional[str] = None


class AccountInfoDto(BaseModel):
    username: str
    name: str
    profile_picture: str

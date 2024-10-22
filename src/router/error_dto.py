from pydantic import BaseModel


class ErrorDto(BaseModel):
    message: str

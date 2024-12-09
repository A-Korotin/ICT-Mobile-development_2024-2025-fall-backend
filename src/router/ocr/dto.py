from typing import List

from pydantic import BaseModel


class PageContents(BaseModel):
    number: int
    content: str

class PdfContents(BaseModel):
    pages: List[PageContents]
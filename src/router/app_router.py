from fastapi import APIRouter
from src.router.auth.auth_router import router as auth_router
from src.router.ocr.ocr_router import router as ocr_router
from src.router.bookmark.bookmark_router import router as bookmark_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(ocr_router, prefix="/ocr", tags=["OCR"])
router.include_router(bookmark_router, prefix="/bookmark", tags=["Bookmark"])

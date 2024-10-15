from fastapi import APIRouter
from src.router.auth.auth_router import router as auth_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["Authentication"])

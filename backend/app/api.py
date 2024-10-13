from fastapi import APIRouter
from app.users import api as users_api

router = APIRouter(prefix="/api/v1")

router.include_router(users_api.router)

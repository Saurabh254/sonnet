from fastapi import APIRouter

from app.users import api as users_api
from app.drivers import api as driver_api
from app.vehicle import api as vehicle_api


router = APIRouter(prefix="/api/v1")

router.include_router(users_api.router)
router.include_router(vehicle_api.router)
router.include_router(driver_api.router)

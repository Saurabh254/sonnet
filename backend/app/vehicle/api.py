from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import auth
from app.database.db import get_async_db
from app.drivers import models as driver_models
from . import errors, interface, schemas

router = APIRouter(tags=["Vehicle Management"], prefix="/vehicles")


@router.post(
    "/register",
    description="Register a new vehicle for the current driver.",
    response_model=schemas.VehicleProfile,
)
async def register_vehicle(
    vehicle_data: schemas.VehicleCreate,
    current_driver: driver_models.Driver = Depends(auth.get_current_active_driver),
    db: AsyncSession = Depends(get_async_db),
):
    return await interface.register_vehicle(vehicle_data, current_driver, db)


@router.get(
    "",
    description="Retrieve a vehicle by its ID.",
    response_model=schemas.VehicleProfile,
)
async def get_vehicle(
    current_driver: driver_models.Driver = Depends(auth.get_current_active_driver),
    db: AsyncSession = Depends(get_async_db),
):
    return await interface.get_vehicle(driver.id, db)


@router.put(
    "/{vehicle_id}",
    description="Update vehicle details by its ID.",
    response_model=schemas.VehicleProfile,
)
async def update_vehicle(
    vehicle_id: str,
    vehicle_data: schemas.VehicleUpdate,
    db: AsyncSession = Depends(get_async_db),
):
    return await interface.update_vehicle(vehicle_id, vehicle_data, db)

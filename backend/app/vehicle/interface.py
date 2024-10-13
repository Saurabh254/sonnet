from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.drivers import models as driver_models

from . import errors, models, schemas


async def register_vehicle(
    vehicle_data: schemas.VehicleCreate, driver: driver_models.Driver, db: AsyncSession
) -> models.Vehicle:
    stmt = select(models.Vehicle).where(
        (models.Vehicle.registration_number == vehicle_data.registration_number)
        | (models.Vehicle.license_number == vehicle_data.license_number)
    )
    result = await db.execute(stmt)
    existing_vehicle = result.scalar_one_or_none()

    if existing_vehicle:
        raise errors.VehicleAlreadyExists

    new_vehicle = models.Vehicle(
        license_number=vehicle_data.license_number,
        registration_number=vehicle_data.registration_number,
        capacity=vehicle_data.capacity,
        location=f'SRID=4326;POINT({vehicle_data.location["longitude"]} {vehicle_data.location["latitude"]})',
        driver_id=driver.id,
    )
    db.add(new_vehicle)
    await db.commit()
    await db.refresh(new_vehicle)
    return new_vehicle


async def get_vehicle(driver_id: str, db: AsyncSession) -> models.Vehicle:
    stmt = select(models.Vehicle).where(models.Vehicle.driver_id == driver_id)
    result = await db.execute(stmt)
    vehicle = result.scalar_one_or_none()
    return vehicle


async def update_vehicle(
    vehicle_id: str, vehicle_data: schemas.VehicleUpdate, db: AsyncSession
) -> models.Vehicle:
    stmt = select(models.Vehicle).where(models.Vehicle.id == vehicle_id)
    result = await db.execute(stmt)
    vehicle = result.scalar_one_or_none()

    if not vehicle:
        raise errors.VehicleNotFound

    # Update vehicle details
    if vehicle_data.license_number:
        vehicle.license_number = vehicle_data.license_number
    if vehicle_data.registration_number:
        vehicle.registration_number = vehicle_data.registration_number
    if vehicle_data.capacity is not None:
        vehicle.capacity = vehicle_data.capacity
    if vehicle_data.location:
        vehicle.location = f'SRID=4326;POINT({vehicle_data.location["longitude"]} {vehicle_data.location["latitude"]})'

    await db.commit()
    await db.refresh(vehicle)
    return vehicle


async def delete_vehicle(vehicle_id: str, db: AsyncSession) -> None:
    stmt = select(models.Vehicle).where(models.Vehicle.id == vehicle_id)
    result = await db.execute(stmt)
    vehicle = result.scalar_one_or_none()

    if not vehicle:
        raise errors.VehicleNotFound

    await db.delete(vehicle)
    await db.commit()


async def update_vehicle_location(
    vehicle_id: str, latitude: float, longitude: float, db: AsyncSession
) -> models.Vehicle:
    stmt = (
        update(models.Vehicle)
        .where(models.Vehicle.id == vehicle_id)
        .values(location=f"SRID=4326;POINT({longitude} {latitude})")
    )
    await db.execute(stmt)
    await db.commit()

    # Fetch the updated vehicle to return
    updated_stmt = select(models.Vehicle).filter(models.Vehicle.id == vehicle_id)
    result = await db.execute(updated_stmt)
    return result.scalar_one_or_none()

from sqlalchemy import select

from typing import Dict
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from geoalchemy2.elements import WKTElement
from app.drivers import models as driver_models
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from . import errors, models, schemas


from geoalchemy2.shape import to_shape


def wkb_to_dict(location) -> Dict[str, float]:
    """Convert WKBElement to a dict containing latitude and longitude."""
    if location is not None:
        point = to_shape(location)  # Convert to a shapely Point object
        return {"latitude": point.y, "longitude": point.x}
    return {"latitude": None, "longitude": None}


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
        location=f"SRID=4326;POINT({vehicle_data.location.longitude} {vehicle_data.location.latitude})",
        driver_id=driver.id,
    )
    db.add(new_vehicle)
    await db.commit()
    await db.refresh(new_vehicle)

    # Convert location to dict before returning
    vehicle_dict = new_vehicle.__dict__.copy()  # Create a dict copy of the vehicle
    vehicle_dict["location"] = wkb_to_dict(new_vehicle.location)  # Convert location

    return vehicle_dict  # Return the serialized dict


async def get_vehicle(driver_id: str, db: AsyncSession) -> models.Vehicle:
    stmt = select(models.Vehicle).where(models.Vehicle.driver_id == driver_id)
    result = await db.execute(stmt)
    vehicle = result.scalar_one_or_none()

    if vehicle:
        # Convert the location to a dictionary
        vehicle_dict = (
            vehicle.__dict__.copy()
        )  # Copy the vehicle's attributes to a dict
        vehicle_dict["location"] = wkb_to_dict(vehicle.location)  # Convert the location
        return vehicle_dict

    return None  # Return None if no vehicle is found


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
        vehicle.location = f"SRID=4326;POINT({vehicle_data.location.longitude} {vehicle_data.location.latitude})"

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


async def get_vehicles_within_radius(
    db: AsyncSession, latitude: float, longitude: float, radius_km: float
) -> list[models.Vehicle]:
    # Create a POINT geometry from the provided latitude and longitude
    reference_point = WKTElement(f"POINT({longitude} {latitude})", srid=4326)

    # Perform the query using ST_DWithin to get vehicles within the given radius
    stmt = (
        select(models.Vehicle)
        .options(joinedload(models.Vehicle.driver))
        .where(
            func.ST_DWithin(
                models.Vehicle.location,  # The location column in the Vehicle model
                reference_point,  # The reference point (WKTElement)
                radius_km * 1000,  # Convert radius to meters
            )
        )
    )

    result = await db.execute(stmt)
    vehicles = result.scalars().all()
    return vehicles

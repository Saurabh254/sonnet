from operator import or_
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from .models import (
    Drive,
    DriveStatus,
)  # Adjust the import according to your project structure
from .schemas import (
    DriveCreate,
    DriveUpdate,
)  # Assuming you have Pydantic models in schemas.py
from app.users import models as user_models
from app.drivers import models as driver_models


async def create_drive(
    user: user_models.User, db: AsyncSession, drive_create: DriveCreate
) -> Drive:
    new_drive = Drive(
        **{
            **drive_create.model_dump(exclude={"user_id", "location"}),
            "user_id": user.id,
            "location": f"SRID=4326;POINT({drive_create.location.longitude} {drive_create.location.latitude})",
        }
    )
    db.add(new_drive)
    await db.commit()
    await db.refresh(new_drive)
    return new_drive


async def update_drive(
    db: AsyncSession,
    drive_id: str,
    drive_update: DriveUpdate,
    user: user_models.User,
) -> Drive:
    stmt = select(Drive).where(Drive.id == drive_id).where(Drive.user_id == user.id)
    result = await db.execute(stmt)
    drive = result.scalar_one_or_none()
    if drive is None:
        raise HTTPException(status_code=404, detail="Drive not found")

    for key, value in drive_update.dict().items():
        if key == "location":
            setattr(
                drive,
                key,
                f"SRID=4326;POINT({value.longitude} {value.latitude})",
            )
        else:
            setattr(drive, key, value)

    await db.commit()
    await db.refresh(drive)
    return drive


async def delete_drive(user: user_models.User, db: AsyncSession, drive_id: str) -> dict:
    stmt = select(Drive).where(Drive.id == drive_id).where(Drive.user_id == user.id)
    result = await db.execute(stmt)
    drive = result.scalar_one_or_none()
    if drive is None:
        raise HTTPException(status_code=404, detail="Drive not found")

    await db.delete(drive)
    await db.commit()
    return {"detail": "Drive deleted successfully"}


async def accept_drive(
    driver: driver_models.Driver, db: AsyncSession, drive_id: str
) -> dict:
    stmt = select(Drive).where(Drive.id == drive_id).where(Drive.user_id == driver.id)
    result = await db.execute(stmt)
    drive = result.scalar_one_or_none()
    if drive is None:
        raise HTTPException(status_code=404, detail="Drive not found")

    drive.status = DriveStatus.ACCEPTED  # type: ignore
    await db.commit()
    return {"detail": "Drive accepted successfully"}


async def reject_drive(
    driver: driver_models.Driver, db: AsyncSession, drive_id: str
) -> dict:
    stmt = select(Drive).filter(Drive.id == drive_id).where(Drive.user_id == driver.id)
    result = await db.execute(stmt)
    drive = result.scalar_one_or_none()
    if drive is None:
        raise HTTPException(status_code=404, detail="Drive not found")

    drive.status = DriveStatus.REJECTED  # type: ignore
    await db.commit()
    return {"detail": "Drive rejected successfully"}


async def get_drive_by_id(
    db: AsyncSession, drive_id: str, user_id: str, driver_id: str
) -> Drive:
    stmt = (
        select(Drive)
        .options(joinedload(Drive.user))
        .where(Drive.id == drive_id)
        .where(or_(Drive.user_id == user_id, Drive.driver_id == driver_id))
    )
    result = await db.execute(stmt)
    drive = result.scalar_one_or_none()
    if drive is None:
        raise HTTPException(status_code=404, detail="Drive not found")
    return drive


async def get_drives_by_driver(
    db: AsyncSession, user: user_models.User
) -> Sequence[Drive]:
    stmt = select(Drive).where(Drive.user_id == user.id).order_by(Drive.created_at)
    result = await db.execute(stmt)
    drives = result.scalars().all()
    return drives

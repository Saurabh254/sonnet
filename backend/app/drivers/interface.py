from typing import overload

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import UnauthorisedUser

from . import errors, models, schemas


async def login_driver(phone: str, otp: str, db: AsyncSession) -> models.Driver:
    if phone[-6:] != otp:
        raise UnauthorisedUser
    stmt = select(models.Driver).where(models.Driver.phone == phone)
    result = await db.execute(stmt)
    driver = result.scalar_one_or_none()

    if not driver:
        raise errors.DriverNotFound

    return driver


async def signup_driver(
    driver_data: schemas.DriverCreate, db: AsyncSession
) -> models.Driver:
    is_existing_stmt = (
        select(func.count())
        .select_from(models.Driver)
        .filter(models.Driver.phone == driver_data.phone)
    )
    result = await db.execute(is_existing_stmt)
    count = result.scalar()
    if count:
        raise errors.DriverAlreadyExists

    driver = models.Driver(**driver_data.model_dump(exclude={"otp"}))
    db.add(driver)
    await db.commit()
    await db.refresh(driver)
    return driver


async def logout_driver(driver: models.Driver) -> dict[str, str]:
    return {"msg": "Successfully logged out"}


async def get_driver(driver_id: str, db: AsyncSession) -> models.Driver:
    stmt = select(models.Driver).filter(models.Driver.id == driver_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

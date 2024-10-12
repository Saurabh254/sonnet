from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from . import models, schemas, errors
from app.exceptions import UnauthorisedUser


async def login_user(phone: str, otp: str, db: AsyncSession) -> models.User:
    if phone[-6:] != otp:
        raise UnauthorisedUser
    stmt = select(models.User).where(models.User.phone == phone)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise errors.UserNotFound

    if not user.active:
        raise UnauthorisedUser

    return user


async def signup_user(user_data: schemas.UserCreate, db: AsyncSession) -> models.User:
    is_existing_stmt = (
        select(func.count())
        .select_from(models.User)
        .filter(models.User.phone == user_data.phone)
    )
    result = await db.execute(is_existing_stmt)
    count = result.scalar()
    if count:
        raise errors.UserAlreadyExists

    user = models.User(**user_data.model_dump())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def logout_user(user: models.User) -> dict[str, str]:
    return {"msg": "Successfully logged out"}


async def get_user(user: models.User) -> models.User:
    return user

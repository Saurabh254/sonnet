from typing import Any

import redis
from fastapi import Cookie, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import auth
from app.database.db import get_async_db
from app.exceptions import InvalidSession, UnauthorisedUser
from app.users import models as user_models
from app.utils.common import get_redis_conn_dep

from app.drivers import models as driver_models


async def _validate_user_id(
    user_id: str = Cookie(None),
) -> str:

    return user_id


async def get_optional_loggedin_user(
    user_id: str = Cookie(None), db: AsyncSession = Depends(get_async_db)
):
    if user_id:
        stmt = select(user_models.User).filter(user_models.User.id == user_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    return None


async def get_optional_loggedin_driver(
    driver_id: str = Cookie(None), db: AsyncSession = Depends(get_async_db)
):
    if driver_id:
        stmt = select(user_models.User).filter(driver_models.Driver.id == driver_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    return None


async def get_current_user(
    user_id: str = Depends(_validate_user_id),
    db: AsyncSession = Depends(get_async_db),
) -> user_models.User:
    stmt = select(user_models.User).filter(user_models.User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()  # This will return the User
    if user is None:
        raise UnauthorisedUser
    return user


async def get_current_active_user(
    user: Any = Depends(get_current_user),
) -> user_models.User:
    if user.active:
        return user
    raise UnauthorisedUser(message="forbidden user")


async def _validate_driver_id(
    driver_id: str = Cookie(None),
) -> str:
    return driver_id


async def get_current_driver(
    driver_id: str = Depends(_validate_driver_id),
    db: AsyncSession = Depends(get_async_db),
) -> driver_models.Driver:
    stmt = select(driver_models.Driver).filter(driver_models.Driver.id == driver_id)
    result = await db.execute(stmt)
    driver = result.scalar_one_or_none()  # This will return the Driver
    if driver is None:
        raise UnauthorisedUser
    return driver


# async def get_current_active_driver(
#     driver: driver_models.Driver = Depends(get_current_driver),
# ) -> driver_models.Driver:
#     if driver.active:
#         return driver
#     raise UnauthorisedUser(message="forbidden driver")

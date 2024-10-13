from typing import Any
from fastapi import Depends, Cookie
from app.exceptions import UnauthorisedUser, InvalidSession
from app.utils.common import get_redis_conn_dep
import redis
from sqlalchemy import select
from app.database.db import get_async_db
from app.users import models as user_models
from sqlalchemy.ext.asyncio import AsyncSession


async def _validate_user_id(
    user_id: str = Cookie(None),
) -> str:

    return user_id


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

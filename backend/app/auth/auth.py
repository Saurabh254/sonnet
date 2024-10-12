from typing import Any
from fastapi import Depends
from app.exceptions import UnauthorisedUser, InvalidSession
from app.utils.common import get_redis_conn_dep
import redis
from .dependency import getSessionIdDep, getUserIdDep


def _check_session_id_validation(
    session_id: getSessionIdDep,
    user_id: getUserIdDep,
    redis_conn: redis.Redis = Depends(get_redis_conn_dep),
) -> bool:
    session_user_id = redis_conn.get(f"session_{session_id}")

    if session_user_id and session_user_id == user_id:
        return True
    return False


def _validate_user_id_with_session_id(
    user_id: getUserIdDep,
    is_valid_session: Any = Depends(_check_session_id_validation),
) -> str:
    if not is_valid_session:
        raise InvalidSession

    return user_id


def get_current_user(user_id: str = Depends(_validate_user_id_with_session_id)):
    return ...


def get_current_active_user(user: Any = Depends(get_current_user)):
    if user.active:
        return user
    raise UnauthorisedUser(message="forbidden user")

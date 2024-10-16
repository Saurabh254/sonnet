from fastapi import (
    APIRouter,
    Body,
    Depends,
    FastAPI,
    WebSocket,
    WebSocketException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sse_starlette import EventSourceResponse
import uvicorn

from app.auth import auth
from app.database.db import get_async_db
from app.users import models as user_models
from . import interface, models, schemas, stream

router = APIRouter(tags=["Driver Authentication"], prefix="/drivers")


@router.websocket("/location/ws")
async def update_driver_location_ws_route(
    websocket: WebSocket,
    db: AsyncSession = Depends(get_async_db),
):

    await websocket.accept()
    try:
        token = await websocket.receive_text()
        driver = await interface.get_driver_from_access_token(token, db)
        if not driver:
            raise
        webstream = stream.RedisStream(driver_id=driver.id)

        while True:
            data = await websocket.receive_text()
            await webstream.publish_driver_location_to_topic(data=data)
    except Exception:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)


@router.get("/{driver_id}/location")
async def get_driver_location(
    driver_id: str,
    current_user: user_models.User = Depends(auth.get_current_active_user),
):

    generator = await interface.get_driver_location(
        driver_id=driver_id, user=current_user
    )
    return EventSourceResponse(content=generator)


@router.post(
    "/login",
    description="Log in the driver with a phone number and OTP to get an access token.",
    response_model=schemas.LoginResponse,
)
async def login(
    phone: str = Body(..., description="Driver's phone number"),
    otp: str = Body(..., description="One-time password sent to the driver's phone"),
    db: AsyncSession = Depends(get_async_db),
):
    return await interface.login_driver(phone, otp, db)


@router.post(
    "/signup",
    description="Sign up a new driver using the provided data.",
    response_model=schemas.DriverProfile,
)
async def signup(
    driver_data: schemas.DriverCreate, db: AsyncSession = Depends(get_async_db)
):
    return await interface.signup_driver(driver_data=driver_data, db=db)


@router.post(
    "/logout",
    description="Logs out the currently authenticated driver and invalidates the session.",
    status_code=204,
)
async def logout(
    current_driver: models.Driver = Depends(auth.get_current_driver),
):
    await interface.logout_driver(current_driver)


@router.get(
    "/me",
    response_model=schemas.DriverProfile,
    description="Retrieve the profile of the currently authenticated driver.",
)
async def read_me(
    current_driver: models.Driver = Depends(auth.get_current_driver),
):
    return current_driver

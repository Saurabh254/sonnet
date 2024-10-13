from fastapi import APIRouter, Body, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import auth
from app.database.db import get_async_db

from . import interface, models, schemas

router = APIRouter(tags=["Driver Authentication"], prefix="/drivers")


@router.post(
    "/login",
    description="Log in the driver with a phone number and OTP to get an access token.",
    response_model=schemas.DriverProfile,
)
async def login(
    response: Response,
    phone: str = Body(..., description="Driver's phone number"),
    otp: str = Body(..., description="One-time password sent to the driver's phone"),
    db: AsyncSession = Depends(get_async_db),
):
    driver = await interface.login_driver(phone, otp, db)
    if not driver:
        return driver
    response.set_cookie("driver_id", str(driver.id))
    return driver


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
    response_model=schemas.DriverProfile,
)
async def logout(
    current_driver: models.Driver = Depends(auth.get_current_driver),
):
    return await interface.logout_driver(current_driver)


@router.get(
    "/me",
    response_model=schemas.DriverProfile,
    description="Retrieve the profile of the currently authenticated driver.",
)
async def read_me(
    current_driver: models.Driver = Depends(auth.get_current_driver),
):
    return current_driver

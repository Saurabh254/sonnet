from fastapi import Body, FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas
from app.auth import auth
from app.database.db import (
    get_async_db,
)  # Adjust import according to your project structure
from . import interface  # Import your interface

app = FastAPI()


@app.post("/login")
async def login(
    phone: str = Body(),
    otp: str = Body(),
    db: AsyncSession = Depends(get_async_db),
):
    return await interface.login_user(phone, otp, db)


@app.post("/logout")
async def logout(current_user: models.User = Depends(auth.get_current_active_user)):
    return await interface.logout_user(current_user)


@app.get("/me", response_model=schemas.UserProfile)
async def read_me(current_user: models.User = Depends(auth.get_current_active_user)):
    return current_user

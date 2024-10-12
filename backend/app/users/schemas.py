from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    name: str
    active: bool


class UserCreate(UserBase):
    phone: str
    otp: str


class UserProfile(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # Allows Pydantic to read data from ORM models

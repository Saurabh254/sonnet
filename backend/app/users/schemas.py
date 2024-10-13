from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    phone: str
    otp: str


class UserProfile(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # Allows Pydantic to read data from ORM models

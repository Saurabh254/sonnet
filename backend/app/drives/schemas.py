from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional

from app.users.schemas import UserProfile


class DriveStatus(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    CANCELED = "canceled"


class DriveCreate(BaseModel):
    driver_id: str
    location: "Location"


class Location(BaseModel):
    longitude: float
    latitude: float


class DriveUpdate(BaseModel):
    driver_id: Optional[str]
    location: Location  # You can define a more specific type if needed
    status: Optional[DriveStatus]  # Status can also be updated


class Driver(BaseModel):
    name: str
    id: str
    created_at: datetime
    updated_at: datetime


class Drive(BaseModel):
    status: DriveStatus
    driver_id: str
    id: str
    user: UserProfile
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # Enables compatibility with SQLAlchemy models

from typing import Dict, Optional

from pydantic import BaseModel, Field


class VehicleBase(BaseModel):
    license_number: str
    registration_number: str
    capacity: int


class Location(BaseModel):
    latitude: float
    longitude: float


class VehicleCreate(VehicleBase):
    location: Location


class VehicleUpdate(BaseModel):
    license_number: Optional[str] = None
    registration_number: Optional[str] = None
    capacity: Optional[int] = None
    location: Location


class VehicleProfile(VehicleBase):
    driver_id: str
    location: Dict[str, float]

    class Config:
        orm_mode = True

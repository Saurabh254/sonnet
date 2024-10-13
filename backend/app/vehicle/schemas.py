from typing import Dict, Optional

from pydantic import BaseModel, Field


class VehicleBase(BaseModel):
    license_number: str
    registration_number: str
    capacity: int


class VehicleCreate(VehicleBase):
    location: Dict[str, float] = Field(
        ..., description="A dictionary with 'latitude' and 'longitude' keys"
    )


class VehicleUpdate(BaseModel):
    license_number: Optional[str] = None
    registration_number: Optional[str] = None
    capacity: Optional[int] = None
    location: Optional[Dict[str, float]] = Field(
        None, description="A dictionary with 'latitude' and 'longitude' keys"
    )


class VehicleProfile(VehicleBase):
    driver_id: str
    location: Dict[str, float]

    class Config:
        orm_mode = True

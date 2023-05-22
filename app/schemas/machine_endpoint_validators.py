from __future__ import annotations

from pydantic import BaseModel
from pydantic import validator
from pydantic import Extra
from pydantic import Field


class MachineBaseSchema(BaseModel):
    """Pydantic validator (schema) for a new machine."""

    class Config:
        extra = Extra.forbid  # forbid extra fields

    name: str = Field(..., min_length=3, max_length=10)
    nominal_power: int
    type: str
    description: str | None

    @validator("type")
    def validate_type(cls, string):
        if string not in ["furnace", "compressor", "chiller", "rolling mill"]:
            raise ValueError("type must be one of furnace, compressor, chiller, rolling mill")
        return string


class SpecificMachineSchema(BaseModel):
    name: str

    class Config:
        extra = Extra.forbid  # forbid extra fields


class MachineDB(MachineBaseSchema):
    machine_id: int
    message: str

    class Config:
        orm_mode = True  # tell pydantic to read the data as if from an ORM, not a dict

from __future__ import annotations

from pydantic import BaseModel
from pydantic import Extra


class MaximumPowerCreateSchema(BaseModel):
    """Pydantic validator (schema) for setting the maximum power for the API.
    Defines a data validation model for maximum power endpoint.
    This makes sure that we receive the data is what we expect.
    """

    class Config:
        extra = Extra.forbid  # forbid extra fields

    maximum_power: int

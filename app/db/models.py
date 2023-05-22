from datetime import datetime

from sqlmodel import Field
from sqlmodel import SQLModel


class Users(SQLModel, table=True):
    """Users table."""

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    phone_number: str = Field(unique=True, index=True)
    first_name: str
    last_name: str
    password: str
    created_at: datetime = Field(default_factory=datetime.now)


class Machines(SQLModel, table=True):
    """Machines table."""

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    nominal_power: int
    type: str
    description: str | None
    created_at: datetime = Field(default_factory=datetime.now)

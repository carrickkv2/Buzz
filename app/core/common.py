from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from jose import jwt
from jose import JWTError
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.connect import get_session
from ..db.operations import get_user_by_id
from .config import Settings
from .security import oauth2_scheme


class TokenData(BaseModel):
    username: int | None = None


settings = Settings()
settings.MAXIMUM_POWER = Settings().MAXIMUM_POWER
settings.TOTAL_POWER = Settings().TOTAL_POWER


async def get_current_user(session: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)):
    """Get's the current logged in user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )

        username: int | None = payload.get("sub", None)
        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception

    user = await get_user_by_id(session, id=token_data.username) if token_data.username else None
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def set_maximum_power(maximum_power: int) -> None:
    """Sets the maximum power of the site."""
    settings.MAXIMUM_POWER = maximum_power


def check_if_maximum_power_is_set() -> bool:
    """Checks if the maximum power of the site is set."""
    if settings.MAXIMUM_POWER is None:
        return False
    return True


def total_power_consumption_of_machines(machine_power: int) -> bool | None:
    """
    Calculates the total power consumption of all the machines
    on site and checks if it exceeds the maximum power.
    """
    if settings.MAXIMUM_POWER is not None:
        if settings.TOTAL_POWER + machine_power > settings.MAXIMUM_POWER:
            return False
    settings.TOTAL_POWER += machine_power
    return True

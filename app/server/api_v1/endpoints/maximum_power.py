import logging

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from ....core.common import get_current_user
from ....core.common import set_maximum_power
from ....db.connect import get_session
from ....schemas.maximum_power_validators import MaximumPowerCreateSchema

log = logging.getLogger("uvicorn")
router = APIRouter()


@router.post("/create", response_model=str, status_code=201)
async def configure_maximum_power(
    maximum_power: MaximumPowerCreateSchema,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    """
    An endpoint to set the maximum power
    that a site has available using a POST request
    """

    if maximum_power.maximum_power < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The maximum power can't be less than 1.",
        )

    set_maximum_power(maximum_power.maximum_power)

    return f"Maximum power of {maximum_power.maximum_power} set successfully."

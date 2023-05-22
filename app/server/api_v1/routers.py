from fastapi import APIRouter

from .endpoints import auth
from .endpoints import maximum_power
from .endpoints import machines


api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(maximum_power.router, prefix="/maximum-power", tags=["maximum_power"])
api_router.include_router(machines.router, prefix="/machines", tags=["machines"])

import logging

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from ....core.common import get_current_user
from ....core.common import check_if_maximum_power_is_set
from ....core.common import total_power_consumption_of_machines
from ....db.connect import get_session
from ....db import operations
from ....schemas.machine_endpoint_validators import MachineBaseSchema
from ....schemas.machine_endpoint_validators import MachineDB
from ....schemas.machine_endpoint_validators import SpecificMachineSchema

log = logging.getLogger("uvicorn")
router = APIRouter()


@router.post("/create", response_model=MachineDB, status_code=201)
async def create_machine(
    machine: MachineBaseSchema,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    """
    An endpoint to create a machine using a POST request
    """

    if not check_if_maximum_power_is_set():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The maximum power of the site has not been set. "
            "Please set it by sending a POST request to the /api/v1/maximum-power endpoint.",
        )

    if total_power_consumption_of_machines(machine.nominal_power) is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The total power consumption of the machines exceeds the maximum power of the site. "
            "Please remove some machines or set the maximum power of the site to a higher value.",
        )

    if await operations.get_machine_by_name(session, name=machine.name) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A machine with the name {machine.name} already exists.",
        )

    try:
        db_response = await operations.add_new_machine_to_db(session, machine)
        db_response = dict(db_response)

        response_object = {
            "machine_id": db_response["id"],
            "message": "Machine added to site successfully",
            "name": machine.name,
            "nominal_power": machine.nominal_power,
            "type": machine.type,
            "description": machine.description,
        }

        return response_object

    except Exception as e:
        log.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error : [ {e} ] occurred while creating the machine.",
        )


@router.get("/get", response_model=MachineDB, status_code=201)
async def read_machine(
    machine: SpecificMachineSchema,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    """
    An endpoint to get a specific machine using the machine name.
    """

    if not check_if_maximum_power_is_set():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The maximum power of the site has not been set. "
            "Please set it by sending a POST request to the /api/v1/maximum-power endpoint.",
        )

    if await operations.get_machine_by_name(session, name=machine.name) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A machine with the name {machine.name} does not exist.",
        )

    try:
        db_response = await operations.get_machine_by_name(session, machine.name)

        if db_response is not None:
            for row in db_response:
                response_object = {
                    "machine_id": row.id,
                    "message": "Successfully retrieved machine details",
                    "name": row.name,
                    "nominal_power": row.nominal_power,
                    "type": row.type,
                    "description": row.description,
                }

                return response_object

    except Exception as e:
        log.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error : [ {e} ] occurred while retrieving the machine.",
        )


@router.put("/update/{name}", response_model=MachineDB, status_code=201)
async def update_machine(
    name: str,
    machine: MachineBaseSchema,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    """
    An endpoint to update a machine using a POST request
    """

    if not check_if_maximum_power_is_set():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The maximum power of the site has not been set. "
            "Please set it by sending a POST request to the /api/v1/maximum-power endpoint.",
        )

    if total_power_consumption_of_machines(machine.nominal_power) is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The total power consumption of the machines exceeds the maximum power of the site. "
            "Can't update the machine. Please remove some machines or set the"
            "maximum power of the site to a higher value.",
        )

    if await operations.get_machine_by_name(session, name) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The machine with the given name does not exist. Please check the name and try again.",
        )

    try:
        db_response = await operations.update_machine(session, machine, name)
        db_response = dict(db_response)

        response_object = {
            "machine_id": db_response["id"],
            "message": "Successfully retrieved machine details",
            "name": machine.name,
            "nominal_power": machine.nominal_power,
            "type": machine.type,
            "description": machine.description,
        }

        return response_object

    except Exception as e:
        log.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error : [ {e} ] occurred while updating the machine.",
        )


@router.delete("/delete", response_model=str, status_code=201)
async def delete_machine(
    machine: SpecificMachineSchema,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    """
    An endpoint to delete a machine using a POST request
    """

    if not check_if_maximum_power_is_set():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The maximum power of the site has not been set. "
            "Please set it by sending a POST request to the /api/v1/maximum-power endpoint.",
        )

    if await operations.get_machine_by_name(session, machine.name) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The machine with the given name does not exist. Please check the name and try again.",
        )

    try:
        await operations.delete_machine(session, machine.name)

        return f"Successfully deleted machine with name {machine.name}"

    except Exception as e:
        log.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error : [ {e} ] occurred while deleting the machine.",
        )

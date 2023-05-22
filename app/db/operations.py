from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..schemas.auth_endpoint_validators import UserSignupSchema
from ..schemas.machine_endpoint_validators import MachineBaseSchema
from .models import Users
from .models import Machines


async def add_new_machine_to_db(db_session: AsyncSession, payload: MachineBaseSchema):
    machine = Machines(
        name=payload.name,
        nominal_power=payload.nominal_power,
        type=payload.type,
        description=payload.description,
    )

    db_session.add(machine)
    await db_session.commit()
    await db_session.refresh(machine)
    return machine


async def get_all_machines(db_session: AsyncSession):
    query = select(Machines)
    results = await db_session.execute(query)
    return results.all()


async def get_machine_by_name(db_session: AsyncSession, name: str):
    query = select(Machines).where(Machines.name == name)
    results = await db_session.execute(query)
    return results.one_or_none()


async def update_machine(db_session: AsyncSession, payload: MachineBaseSchema, name: str):
    query = select(Machines).where(Machines.name == name)
    results = await db_session.execute(query)
    machine = results.one()
    machine[0].name = payload.name
    machine[0].nominal_power = payload.nominal_power
    machine[0].type = payload.type
    machine[0].description = payload.description
    db_session.add(machine[0])
    await db_session.commit()
    await db_session.refresh(machine[0])
    return machine[0]


async def delete_machine(db_session: AsyncSession, name: str):
    query = select(Machines).where(Machines.name == name)
    results = await db_session.execute(query)
    machine = results.one()
    await db_session.delete(machine[0])
    await db_session.commit()
    return machine[0]


async def add_new_user_to_db(db_session: AsyncSession, payload: UserSignupSchema):
    user = Users(
        email=payload.email,
        password=payload.password,
        phone_number=payload.phone_number,
        first_name=payload.first_name,
        last_name=payload.last_name,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


async def get_user_by_email(db_session: AsyncSession, email: str):
    query = select(Users).where(Users.email == email)
    results = await db_session.execute(query)
    return results.one_or_none()


async def get_user_by_phone_number(db_session: AsyncSession, phone_number: str):
    query = select(Users).where(Users.phone_number == phone_number)
    results = await db_session.execute(query)
    return results.one_or_none()


async def get_user_by_id(db_session: AsyncSession, id: int):
    query = select(Users).where(Users.id == id)
    results = await db_session.execute(query)
    return results.one_or_none()

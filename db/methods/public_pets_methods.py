from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.pet import Pet
from ..engine import connection
from .find_pets_helper import _find_pets


@connection
async def public_find_pets(
    session: AsyncSession,
    type_: Optional[str] = None,
    name: Optional[str] = None,
    breed: Optional[str] = None,
    color: Optional[str] = None,
    min_age: Optional[float] = None,
    max_age: Optional[float] = None,
) -> List[Pet]:
    """
    Search pets by public fields only.
    """

    return await _find_pets(
        session,
        include_secret=False,
        type_=type_,
        name=name,
        breed=breed,
        color=color,
        min_age=min_age,
        max_age=max_age,
    )


@connection
async def public_get_pet_details(session: AsyncSession, pet_id: int) -> Optional[Pet]:
    """
    Retrieve detailed pet info by ID, excluding secret_info.
    """
    pet = await session.get(Pet, pet_id)
    if pet:
        pet.secret_info = None
    return pet

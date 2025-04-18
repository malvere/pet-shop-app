from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from ..models.pet import Pet
from ..engine import connection
from .find_pets_helper import _find_pets


@connection
async def admin_create_pet(session: AsyncSession, data: Dict[str, Any]) -> Optional[Pet]:
    """
    Create a new pet. Expects all public fields plus optional secret_info.
    """
    try:
        pet = Pet(
            type=data["type"],
            name=data["name"],
            breed=data["breed"],
            color=data["color"],
            age=data["age"],
            secret_info=data.get("secret_info"),
        )
        session.add(pet)
        await session.commit()
        await session.refresh(pet)
        return pet
    except Exception as e:
        print("Error creating pet:", e)
        await session.rollback()
        return None


@connection
async def admin_update_pet(session: AsyncSession, pet_id: int, data: Dict[str, Any]) -> Optional[Pet]:
    """
    Update an existing pet by ID.
    """

    try:
        pet = await session.get(Pet, pet_id)
        if not pet:
            return None
        for field in ["type", "name", "breed", "color", "age", "secret_info"]:
            if field in data:
                setattr(pet, field, data[field])
        await session.commit()
        await session.refresh(pet)
        return pet
    except SQLAlchemyError as e:
        print(f"Error updating pet: {e}")
        await session.rollback()
        return None


@connection
async def admin_delete_pet(session: AsyncSession, pet_id: int) -> bool:
    """
    Delete a pet by ID.
    """
    try:
        pet = await session.get(Pet, pet_id)
        if not pet:
            return False
        session.delete(pet)
        await session.commit()
        return True
    except SQLAlchemyError as e:
        print(f"Error deleting pet: {e}")
        await session.rollback()
        return False


@connection
async def admin_find_pets(
    session: AsyncSession,
    type_: Optional[str] = None,
    name: Optional[str] = None,
    breed: Optional[str] = None,
    color: Optional[str] = None,
    min_age: Optional[float] = None,
    max_age: Optional[float] = None,
    secret_info: Optional[str] = None,
) -> List[Pet]:
    """
    Search pets by any field, including secret_info.
    """

    return await _find_pets(
        session,
        include_secret=True,
        type_=type_,
        name=name,
        breed=breed,
        color=color,
        min_age=min_age,
        max_age=max_age,
        secret_info=secret_info,
    )


@connection
async def admin_get_pet_details(session: AsyncSession, pet_id: int) -> Optional[Pet]:
    """
    Retrieve full pet details by ID, including secret_info.
    """
    return await session.get(Pet, pet_id)

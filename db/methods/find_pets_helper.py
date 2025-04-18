from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_
from sqlalchemy.future import select

from ..models.pet import Pet


async def _find_pets(
    session: AsyncSession,
    *,
    include_secret: bool,
    type_: Optional[str] = None,
    name: Optional[str] = None,
    breed: Optional[str] = None,
    color: Optional[str] = None,
    min_age: Optional[float] = None,
    max_age: Optional[float] = None,
    secret_info: Optional[str] = None,
) -> List[Pet]:
    """
    Helper function to search for pets in the database based on various criteria.

    Args:
        session (AsyncSession): The database session.
        include_secret (bool): Whether to include filters for secret information.
        type_ (Optional[str]): The type of pet to filter by.
        name (Optional[str]): The name of the pet to filter by (partial match).
        breed (Optional[str]): The breed of the pet to filter by (partial match).
        color (Optional[str]): The color of the pet to filter by (partial match).
        min_age (Optional[float]): The minimum age of the pet to filter by.
        max_age (Optional[float]): The maximum age of the pet to filter by.
        secret_info (Optional[str]): Secret information to filter by (partial match), only applied if include_secret is True.

    Returns:
        List[Pet]: A list of pets that match the provided criteria.
    """
    stmt = select(Pet)
    filters = []

    if type_:
        filters.append(Pet.type == type_)
    if name:
        filters.append(Pet.name.ilike(f"%{name}%"))
    if breed:
        filters.append(Pet.breed.ilike(f"%{breed}%"))
    if color:
        filters.append(Pet.color.ilike(f"%{color}%"))
    if min_age is not None:
        filters.append(Pet.age >= min_age)
    if max_age is not None:
        filters.append(Pet.age <= max_age)

    # only apply secret filter when admin wants it
    if include_secret and secret_info:
        filters.append(Pet.secret_info.ilike(f"%{secret_info}%"))

    if filters:
        stmt = stmt.where(and_(*filters))

    result = await session.execute(stmt)
    pets = result.scalars().all()

    return pets

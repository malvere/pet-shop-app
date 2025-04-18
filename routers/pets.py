from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from schemas import PublicPetResponse

from db.methods.public_pets_methods import public_find_pets, public_get_pet_details

pets_router = APIRouter(
    prefix="/pets",
    tags=["public"],
    responses={404: {"description": "Not found"}},
)


@pets_router.get("/find")
async def find_pets(
    type: Optional[str] = None,
    name: Optional[str] = None,
    breed: Optional[str] = None,
    color: Optional[str] = None,
    min_age: Optional[float] = None,
    max_age: Optional[float] = None,
) -> List[PublicPetResponse]:
    pets = await public_find_pets(type, name, breed, color, min_age, max_age)
    return pets


@pets_router.get("/details")
async def get_pet_details(
    pet_id: int,
) -> PublicPetResponse:
    pet = await public_get_pet_details(pet_id)
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
    return pet

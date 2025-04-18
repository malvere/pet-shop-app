from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from schemas import PetCreate, PrivatePetResponse, PetUpdate
from .dependencies import get_current_user

from db import (
    admin_create_pet,
    admin_update_pet,
    admin_delete_pet,
    admin_find_pets,
    admin_get_pet_details,
)

admin_router = APIRouter(
    prefix="/admin/pets",
    tags=["admin"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)


@admin_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_pet(
    pet_in: PetCreate,
) -> PrivatePetResponse:
    pet = await admin_create_pet(pet_in.model_dump())
    return pet


@admin_router.put("/{pet_id}")
async def update_pet(
    pet_id: int,
    pet_in: PetUpdate,
) -> PrivatePetResponse:
    pet = await admin_update_pet(pet_id, pet_in.model_dump(exclude_unset=True))
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
    return pet


@admin_router.delete("/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pet(
    pet_id: int,
):
    success = await admin_delete_pet(pet_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")


@admin_router.get("/")
async def find_pets(
    type: Optional[str] = None,
    name: Optional[str] = None,
    breed: Optional[str] = None,
    color: Optional[str] = None,
    min_age: Optional[float] = None,
    max_age: Optional[float] = None,
    secret_info: Optional[str] = None,
) -> List[PrivatePetResponse]:
    pets = await admin_find_pets(type, name, breed, color, min_age, max_age, secret_info)
    return pets


@admin_router.get("/{pet_id}")
async def get_pet_details(
    pet_id: int,
) -> PrivatePetResponse:
    pet = await admin_get_pet_details(pet_id)
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
    return pet

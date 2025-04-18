# Pydantic schemas

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class RegisterRequest(BaseModel):
    login: str
    password: str


class LoginRequest(BaseModel):
    login: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PetBase(BaseModel):
    type: str = Field(..., examples=["dog"])
    name: str = Field(..., examples=["Bobik"])
    breed: str = Field(..., examples=["Breadless"])
    color: str = Field(..., examples=["yellow"])
    age: float = Field(..., examples=[3.5])
    model_config = ConfigDict(from_attributes=True)


class PetCreate(PetBase):
    secret_info: Optional[str] = Field(None, examples=["mutant"])


class PetUpdate(BaseModel):
    type: Optional[str] = None
    name: Optional[str] = None
    breed: Optional[str] = None
    color: Optional[str] = None
    age: Optional[float] = None
    secret_info: Optional[str] = None


class PrivatePetResponse(PetBase):
    id: int
    secret_info: Optional[str]


class PublicPetResponse(PetBase):
    id: int

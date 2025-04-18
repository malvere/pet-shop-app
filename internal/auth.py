from fastapi import APIRouter, HTTPException, status
from datetime import datetime, timedelta
import jwt

from db.methods.auth_methods import create_user, authenticate_user
from config import conf
from schemas import TokenResponse, RegisterRequest, LoginRequest


auth_router = APIRouter(prefix="/auth", tags=["auth"])


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=conf.jwt.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, conf.jwt.secret_key, algorithm=conf.jwt.algorithm)


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    req: RegisterRequest,
):
    user = await create_user(req.login, req.password)
    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Registration failed")
    # access_token = create_access_token({"sub": user.login})
    return {"status": "success", "login": user.login}


@auth_router.post("/login", response_model=TokenResponse)
async def login_user(
    req: LoginRequest,
):
    user = await authenticate_user(req.login, req.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token({"sub": user.login})
    return {"access_token": access_token, "token_type": "bearer"}

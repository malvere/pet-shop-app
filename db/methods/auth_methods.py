import bcrypt
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from ..models.user import User
from ..engine import connection


@connection
async def create_user(session: AsyncSession, login: str, password: str) -> Optional[User]:
    """
    Create a new user with a salted+hashed password.
    """
    try:
        salt = bcrypt.gensalt()  # type: bytes
        password_hash = bcrypt.hashpw(password.encode("utf-8"), salt)
        user = User(
            login=login,
            salt=salt.decode("utf-8"),
            password_hash=password_hash.decode("utf-8"),
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    except SQLAlchemyError as e:
        print(f"Error creating user: {e}")
        await session.rollback()
        return None


@connection
async def authenticate_user(session: AsyncSession, login: str, password: str) -> Optional[User]:
    """
    Verify a user's credentials. Returns the user if valid, else None.
    """
    result = await session.execute(select(User).filter_by(login=login))
    user = result.scalar_one_or_none()
    if not user:
        return None
    expected_hash = user.password_hash.encode("utf-8")
    if bcrypt.checkpw(password.encode("utf-8"), expected_hash):
        return user
    return None

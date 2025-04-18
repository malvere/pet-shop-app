from sqlalchemy import String, Float, Text
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class Pet(Base):
    __tablename__ = "pets"

    type: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    breed: Mapped[str] = mapped_column(String(100), nullable=False)
    color: Mapped[str] = mapped_column(String(50), nullable=False)
    age: Mapped[float] = mapped_column(Float, nullable=False)
    secret_info: Mapped[str] = mapped_column(Text, nullable=True)

    def __repr__(self):
        return f"<Pet id={self.id} name={self.name} type={self.type}>"

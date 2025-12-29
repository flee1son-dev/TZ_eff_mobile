from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from backend.core.database import Base
from pydantic import EmailStr
from typing import Optional

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    first_name: Mapped[str] = mapped_column(nullable=False)

    last_name: Mapped[str] = mapped_column(nullable=False)

    email: Mapped[EmailStr] = mapped_column(nullable=False, unique=True)

    password: Mapped[str] = mapped_column(nullable=False)

    permissions: Mapped[str] = mapped_column(nullable=False)

    is_active: Mapped[bool] = mapped_column(nullable=False)

    director_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)

    director = relationship(
        "User",
        remote_side=[id],
        back_populates="workers"
    )

    workers = relationship(
        "User",
        back_populates="director"
    )
from sqlalchemy.orm import Mapped, mapped_column
from backend.core.database import Base
from pydantic import EmailStr

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    first_name: Mapped[str] = mapped_column(nullable=False)

    last_name: Mapped[str] = mapped_column(nullable=False)

    email: Mapped[EmailStr] = mapped_column(nullable=False, unique=True)

    password: Mapped[str] = mapped_column(nullable=False)
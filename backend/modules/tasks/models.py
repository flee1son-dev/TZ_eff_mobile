from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from backend.core.database import Base
from typing import Optional

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    title: Mapped[str] = mapped_column(nullable=False)

    description: Mapped[Optional[str]] = mapped_column(nullable=True)

    worker_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    worker = relationship(
        "User",
        back_populates="tasks"
    )
from datetime import datetime

from sqlalchemy import func, String
from sqlalchemy.orm import Mapped, mapped_column

from .base_model import Base


class AdminModel(Base):
    __tablename__ = "admins"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    invite_hash: Mapped[int]
    invite_date: Mapped[datetime] = mapped_column(default=func.now())

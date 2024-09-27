from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base_model import Base


class OperatorModel(Base):
    __tablename__ = "operators"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str]

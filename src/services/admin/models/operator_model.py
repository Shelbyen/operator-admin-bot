from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base_model import Base


class OperatorModel(Base):
    __tablename__ = "operators"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str]

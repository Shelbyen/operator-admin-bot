from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base_model import Base


class ChatModel(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str]

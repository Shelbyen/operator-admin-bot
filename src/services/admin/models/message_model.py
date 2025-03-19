from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base_model import Base


class MessageModel(Base):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    chat_id: Mapped[str] = mapped_column(ForeignKey('chats.id', ondelete='CASCADE'))
    phone: Mapped[str] = mapped_column(String, primary_key=True)
    message: Mapped[str] = mapped_column(Text)

from pydantic import BaseModel


class MessageBase(BaseModel):
    id: str
    chat_id: str
    phone: str
    message: str


class MessageCreate(MessageBase):
    pass


class MessageUpdate(MessageBase):
    pass


class MessageResponse(MessageBase):
    pass


class MessageListResponse(MessageBase):
    pass

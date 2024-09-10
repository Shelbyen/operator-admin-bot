from datetime import datetime

from pydantic import BaseModel


class AdminBase(BaseModel):
    id: int
    invite_hash: int
    invite_date: datetime


class AdminCreate(BaseModel):
    id: int
    invite_hash: int


class AdminUpdate(BaseModel):
    invite_hash: int
    invite_date: datetime


class AdminResponse(AdminBase):
    pass


class AdminListResponse(AdminBase):
    pass

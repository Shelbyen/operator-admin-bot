from pydantic import BaseModel


class OperatorBase(BaseModel):
    id: str
    name: str


class OperatorCreate(OperatorBase):
    pass


class OperatorUpdate(OperatorBase):
    pass


class OperatorResponse(OperatorBase):
    pass


class OperatorListResponse(OperatorBase):
    pass

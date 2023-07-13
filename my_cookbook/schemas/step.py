from typing import Optional

from pydantic import BaseModel


class StepBase(BaseModel):
    name: str
    recipe_item_id: int
    order: int
    description: str


class StepCreate(StepBase):
    pass


class StepUpdate(StepBase):
    name: Optional[str]
    order: Optional[int]
    description: Optional[str]


class StepOrderUpdate(BaseModel):
    id: Optional[int]
    order: Optional[int]


class StepInDBBase(StepBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class Step(StepInDBBase):
    pass


class StepInDB(StepInDBBase):
    pass

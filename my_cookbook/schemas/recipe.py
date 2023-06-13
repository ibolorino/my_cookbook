from pydantic import BaseModel
from typing import Optional


class RecipeBase(BaseModel):
    name: str
    duration: str
    serves: int


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(RecipeBase):
    name: Optional[str]
    duration: Optional[str]
    serves: Optional[int]


class RecipeInDBBase(RecipeBase):
    id: Optional[int] = None
    owner_id: int

    class Config:
        orm_mode = True


class Recipe(RecipeInDBBase):
    pass


class RecipeInDB(RecipeInDBBase):
    pass

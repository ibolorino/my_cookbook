from pydantic import BaseModel
from typing import Optional, List
from .recipe_item import RecipeItem


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
    items: List[RecipeItem]


class RecipeInDB(RecipeInDBBase):
    pass

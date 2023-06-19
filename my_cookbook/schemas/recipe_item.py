from pydantic import BaseModel
from typing import Optional, List
from .step import Step
from .ingredient import Ingredient


class RecipeItemBase(BaseModel):
    name: str
    

class RecipeItemCreate(RecipeItemBase):
    recipe_id: int


class RecipeItemUpdate(RecipeItemBase):
    name: Optional[str]


class RecipeItemInDBBase(RecipeItemBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class RecipeItem(RecipeItemInDBBase):
    steps: List[Step]
    ingredients: List[Ingredient]


class RecipeItemInDB(RecipeItemInDBBase):
    pass

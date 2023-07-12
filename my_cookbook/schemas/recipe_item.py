from typing import List, Optional

from pydantic import BaseModel

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

    def dict(self, **data):
        data = super().dict(**data)
        if "steps" in data and len(data["steps"]) > 1:
            data["steps"] = sorted(data["steps"], key=lambda step: step["order"])
        return data


class RecipeItemInDB(RecipeItemInDBBase):
    pass

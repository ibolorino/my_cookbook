from typing import Optional

from pydantic import BaseModel


class IngredientBase(BaseModel):
    name: str
    recipe_item_id: int
    quantity: str


class IngredientCreate(IngredientBase):
    pass


class IngredientUpdate(IngredientBase):
    name: Optional[str]
    quantity: Optional[str]


class IngredientInDBBase(IngredientBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class Ingredient(IngredientInDBBase):
    pass


class IngredientInDB(IngredientInDBBase):
    pass

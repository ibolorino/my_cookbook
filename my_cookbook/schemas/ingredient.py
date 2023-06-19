from pydantic import BaseModel
from typing import Optional


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

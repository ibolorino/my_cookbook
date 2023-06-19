from pydantic import BaseModel
from typing import Optional


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
    pass


class RecipeItemInDB(RecipeItemInDBBase):
    pass

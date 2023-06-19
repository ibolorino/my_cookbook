from .base import CRUDBase
from my_cookbook.models.recipe import (
    Recipe, 
    RecipeItem,
)
from my_cookbook.schemas.recipe import (
    RecipeCreate,
    RecipeUpdate,
)
from my_cookbook.schemas.recipe_item import (
    RecipeItemCreate,
    RecipeItemUpdate
)
from sqlalchemy.orm import Session
from typing import Any


class CRUDRecipe(CRUDBase[Recipe, RecipeCreate, RecipeUpdate]):
    pass


class CRUDRecipeItem(CRUDBase[RecipeItem, RecipeItemCreate, RecipeItemUpdate]):
    pass


recipe = CRUDRecipe(Recipe)
recipe_item = CRUDRecipeItem(RecipeItem)
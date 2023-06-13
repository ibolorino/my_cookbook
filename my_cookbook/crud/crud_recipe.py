from .base import CRUDBase
from my_cookbook.models.recipe import Recipe
from my_cookbook.schemas.recipe import RecipeCreate, RecipeUpdate
from sqlalchemy.orm import Session
from typing import Any


class CRUDRecipe(CRUDBase[Recipe, RecipeCreate, RecipeUpdate]):
    pass


recipe = CRUDRecipe(Recipe)
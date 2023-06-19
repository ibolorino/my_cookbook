from .base import CRUDBase
from my_cookbook.models.recipe import (
    Recipe, 
    RecipeItem,
    Step,
    Ingredient,
)
from my_cookbook.schemas.recipe import (
    RecipeCreate,
    RecipeUpdate,
)
from my_cookbook.schemas.recipe_item import (
    RecipeItemCreate,
    RecipeItemUpdate,
)
from my_cookbook.schemas.step import (
    StepCreate,
    StepUpdate,
)
from my_cookbook.schemas.ingredient import (
    IngredientCreate,
    IngredientUpdate,
)
from sqlalchemy.orm import Session
from typing import Any


class CRUDRecipe(CRUDBase[Recipe, RecipeCreate, RecipeUpdate]):
    pass


class CRUDRecipeItem(CRUDBase[RecipeItem, RecipeItemCreate, RecipeItemUpdate]):
    pass


class CRUDStep(CRUDBase[Step, StepCreate, StepUpdate]):
    pass


class CRUDIngredient(CRUDBase[Ingredient, IngredientCreate, IngredientUpdate]):
    pass


recipe = CRUDRecipe(Recipe)
recipe_item = CRUDRecipeItem(RecipeItem)
step = CRUDStep(Step)
ingredient = CRUDIngredient(Ingredient)
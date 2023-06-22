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
    StepOrderUpdate,
)
from my_cookbook.schemas.ingredient import (
    IngredientCreate,
    IngredientUpdate,
)
from sqlalchemy import update
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import StaleDataError
from fastapi import HTTPException
from typing import Any, List


class CRUDRecipe(CRUDBase[Recipe, RecipeCreate, RecipeUpdate]):
    pass


class CRUDRecipeItem(CRUDBase[RecipeItem, RecipeItemCreate, RecipeItemUpdate]):
    def update_steps(self, db: Session, *, recipe_item: RecipeItem, steps: List[StepOrderUpdate]) -> RecipeItem:
        db.execute(update(Step), steps)
        db.commit()
        db.refresh(recipe_item)
        return recipe_item
        


class CRUDStep(CRUDBase[Step, StepCreate, StepUpdate]):
    def get_multi(self, db: Session) -> List[Step]:
        return db.query(Step).order_by("order").all()


class CRUDIngredient(CRUDBase[Ingredient, IngredientCreate, IngredientUpdate]):
    pass


recipe = CRUDRecipe(Recipe)
recipe_item = CRUDRecipeItem(RecipeItem)
step = CRUDStep(Step)
ingredient = CRUDIngredient(Ingredient)
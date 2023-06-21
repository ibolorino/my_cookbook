from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from my_cookbook import schemas, crud, models
from my_cookbook.api.dependencies import get_db, get_current_active_user
from sqlalchemy.orm import Session
from my_cookbook.config import get_settings

settings = get_settings()


router = APIRouter(prefix="/ingredient")

@router.get("/", response_model=List[schemas.Ingredient])
def read_ingredients(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    ingredients = crud.ingredient.get_multi(db, skip=skip, limit=limit)
    return ingredients

@router.post("/", response_model=schemas.Ingredient)
def create_ingredient(ingredient_in: schemas.IngredientCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)) -> Any:
    recipe_item = crud.recipe_item.get(db=db, id=ingredient_in.recipe_item_id)
    if recipe_item: # só permite a criação se o current_user for o dono do Recipe
        if recipe_item.recipe.owner_id != current_user.id:
            raise HTTPException(status_code=400, detail="Not enough permissions")
    ingredient = crud.ingredient.create(db, obj_in=ingredient_in,)
    return ingredient

@router.put("/{id}", response_model=schemas.Ingredient)
def update_ingredient(*, db: Session = Depends(get_db), id: int, ingredient_in: schemas.IngredientUpdate, current_user: models.User = Depends(get_current_active_user)) -> Any:
    ingredient = crud.ingredient.get(db=db, id=id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    if not crud.user.is_superuser(current_user) and ingredient.recipe_item.recipe.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    ingredient = crud.ingredient.update(db=db, db_obj=ingredient, obj_in=ingredient_in)
    return ingredient

@router.delete("/{id}", response_model=schemas.Ingredient)
def delete_ingredient(*, db: Session = Depends(get_db), id: int, current_user: models.User = Depends(get_current_active_user)) -> Any:
    ingredient = crud.ingredient.get(db=db, id=id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    if not crud.user.is_superuser(current_user) and ingredient.recipe_item.recipe.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    ingredient = crud.ingredient.remove(db=db, db_obj=ingredient)
    return ingredient

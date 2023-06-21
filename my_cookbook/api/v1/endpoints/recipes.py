from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from my_cookbook import schemas, crud, models
from my_cookbook.api.dependencies import get_db, get_current_active_user
from sqlalchemy.orm import Session
from my_cookbook.config import get_settings

settings = get_settings()


router = APIRouter(prefix="/recipe")

@router.get("/", response_model=List[schemas.Recipe])
def read_recipes(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    recipes = crud.recipe.get_multi(db, skip=skip, limit=limit)
    return recipes

@router.post("/", response_model=schemas.Recipe)
def create_recipe(recipe_in: schemas.RecipeCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)) -> Any:
    recipe = crud.recipe.create(db, obj_in=recipe_in, owner_id=current_user.id)
    return recipe

@router.put("/{id}", response_model=schemas.Recipe)
def update_recipe(*, db: Session = Depends(get_db), id: int, recipe_in: schemas.RecipeUpdate, current_user: models.User = Depends(get_current_active_user)) -> Any:
    recipe = crud.recipe.get(db=db, id=id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    if not crud.user.is_superuser(current_user) and (recipe.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    recipe = crud.recipe.update(db=db, db_obj=recipe, obj_in=recipe_in)
    return recipe

@router.delete("/{id}", response_model=schemas.Recipe)
def delete_recipe(*, db: Session = Depends(get_db), id: int, current_user: models.User = Depends(get_current_active_user)) -> Any:
    recipe = crud.recipe.get(db=db, id=id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    if not crud.user.is_superuser(current_user) and (recipe.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    recipe = crud.recipe.remove(db=db, db_obj=recipe)
    return recipe

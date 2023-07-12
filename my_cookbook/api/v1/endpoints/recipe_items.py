from typing import Any, List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from my_cookbook import crud, models, schemas
from my_cookbook.config import get_settings
from my_cookbook.api.dependencies import get_db, get_current_active_user

settings = get_settings()


router = APIRouter(prefix="/recipe_item")


@router.get("/", response_model=List[schemas.RecipeItem])
def read_recipe_items(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> Any:
    recipe_items = crud.recipe_item.get_multi(db, skip=skip, limit=limit)
    return recipe_items


@router.post("/", response_model=schemas.RecipeItem)
def create_recipe_item(
    recipe_item_in: schemas.RecipeItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    recipe = crud.recipe.get(db=db, id=recipe_item_in.recipe_id)
    if recipe:  # só permite a criação se o current_user for o dono do Recipe
        if recipe.owner_id != current_user.id:
            raise HTTPException(status_code=400, detail="Not enough permissions")

    recipe_item = crud.recipe_item.create(db, obj_in=recipe_item_in)
    return recipe_item


@router.put("/{id}", response_model=schemas.RecipeItem)
def update_recipe_item(
    *,
    db: Session = Depends(get_db),
    id: int,
    recipe_item_in: schemas.RecipeItemUpdate,
    current_user: models.User = Depends(get_current_active_user)
) -> Any:
    recipe_item = crud.recipe_item.get(db=db, id=id)
    if not recipe_item:
        raise HTTPException(status_code=404, detail="Recipe item not found")
    if (
        not crud.user.is_superuser(current_user)
        and recipe_item.recipe.owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    recipe_item = crud.recipe_item.update(
        db=db, db_obj=recipe_item, obj_in=recipe_item_in
    )
    return recipe_item


@router.delete("/{id}", response_model=schemas.RecipeItem)
def delete_recipe_item(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: models.User = Depends(get_current_active_user)
) -> Any:
    recipe_item = crud.recipe_item.get(db=db, id=id)
    if not recipe_item:
        raise HTTPException(status_code=404, detail="Recipe not found")
    if not crud.user.is_superuser(current_user) and (
        recipe_item.recipe.owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    recipe_item = crud.recipe_item.remove(db=db, db_obj=recipe_item)
    return recipe_item


@router.put("/{id}/steps", response_model=schemas.RecipeItem)
def update_recipe_item_steps(
    *,
    db: Session = Depends(get_db),
    id: int,
    steps_in: List[schemas.StepOrderUpdate],
    current_user: models.User = Depends(get_current_active_user)
) -> Any:
    recipe_item = crud.recipe_item.get(db=db, id=id)
    if not recipe_item:
        raise HTTPException(status_code=404, detail="Recipe item not found")
    if recipe_item.recipe.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    recipe_item_steps = [step.id for step in recipe_item.steps]
    steps_in = [
        step.dict(exclude_unset=True)
        for step in steps_in
        if step.id in recipe_item_steps
    ]
    recipe_item = crud.recipe_item.update_steps(
        db=db, recipe_item=recipe_item, steps=steps_in
    )
    return recipe_item

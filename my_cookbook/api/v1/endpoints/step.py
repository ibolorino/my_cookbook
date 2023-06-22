from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from my_cookbook import schemas, crud, models
from my_cookbook.api.dependencies import get_db, get_current_active_user
from sqlalchemy.orm import Session
from my_cookbook.config import get_settings

settings = get_settings()


router = APIRouter(prefix="/step")

@router.get("/", response_model=List[schemas.Step])
def read_steps(
    db: Session = Depends(get_db)
) -> Any:
    steps = crud.step.get_multi(db)
    return steps

@router.post("/", response_model=schemas.Step)
def create_step(step_in: schemas.StepCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)) -> Any:
    recipe_item = crud.recipe_item.get(db=db, id=step_in.recipe_item_id)
    if recipe_item: # só permite a criação se o current_user for o dono do Recipe
        if recipe_item.recipe.owner_id != current_user.id:
            raise HTTPException(status_code=400, detail="Not enough permissions")
    step = crud.step.create(db, obj_in=step_in,)
    return step

@router.put("/{id}", response_model=schemas.Step)
def update_step(*, db: Session = Depends(get_db), id: int, step_in: schemas.StepUpdate, current_user: models.User = Depends(get_current_active_user)) -> Any:
    step = crud.step.get(db=db, id=id)
    if not step:
        raise HTTPException(status_code=404, detail="Step not found")
    if not crud.user.is_superuser(current_user) and step.recipe_item.recipe.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    step = crud.step.update(db=db, db_obj=step, obj_in=step_in)
    return step

@router.delete("/{id}", response_model=schemas.Step)
def delete_step(*, db: Session = Depends(get_db), id: int, current_user: models.User = Depends(get_current_active_user)) -> Any:
    step = crud.step.get(db=db, id=id)
    if not step:
        raise HTTPException(status_code=404, detail="Step not found")
    if not crud.user.is_superuser(current_user) and step.recipe_item.recipe.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    step = crud.step.remove(db=db, db_obj=step)
    return step

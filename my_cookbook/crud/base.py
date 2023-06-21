from typing import Generic, Type, TypeVar, Optional, List, Any, Union, Dict
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from my_cookbook.db.base_class import Base
from sqlalchemy.orm import Session

from sqlalchemy.exc import IntegrityError


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: CreateSchemaType, owner_id: Optional[int] = None) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        if owner_id:
            obj_in_data.update({"owner_id": owner_id})
        db_obj = self.model(**obj_in_data)
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError as ie:
            message = ie.orig.diag.message_detail.replace('"', "'")
            if message:
                raise HTTPException(status_code=400, detail=message)
            raise ie
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"{e.__class__.__name__}: {str(e)}")
    
    def update(self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError as ie:
            message = ie.orig.diag.message_detail.replace('"', "'")
            if message:
                raise HTTPException(status_code=400, detail=message)
            raise ie
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"{e.__class__.__name__}: {str(e)}")
    
    def remove(self, db: Session, *, db_obj: ModelType) -> ModelType:
        db.delete(db_obj)
        db.commit()
        return(db_obj)
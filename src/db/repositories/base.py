from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.db.database import Base


ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, db_session: Session, model: Type[ModelType]):
        self.db_session = db_session
        self.model = model

    def get_all(self) -> List[ModelType]:
        return self.db_session.query(self.model).all()

    def get_by_id(self, id: int) -> Optional[ModelType]:
        return self.db_session.query(self.model).filter(self.model.id == id).first()

    def create(self, obj_in: dict) -> ModelType:
        try:
            db_obj = self.model(**obj_in)
            self.db_session.add(db_obj)
            self.db_session.commit()
            self.db_session.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise e

    def update(self, id: int, obj_in: dict) -> Optional[ModelType]:
        try:
            db_obj = self.get_by_id(id)
            if not db_obj:
                return None
            for key, value in obj_in.items():
                setattr(db_obj, key, value)
            self.db_session.commit()
            self.db_session.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise e

    def delete(self, id: int) -> bool:
        try:
            db_obj = self.get_by_id(id)
            if not db_obj:
                return False
            self.db_session.delete(db_obj)
            self.db_session.commit()
            return True
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise e

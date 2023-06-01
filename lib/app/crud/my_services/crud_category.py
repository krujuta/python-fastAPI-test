from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from lib.app.crud.base import CRUDBase
from lib.app.models.my_services import Category
from lib.app.schemas.my_services.category import CategoryCreate, CategoryUpdate


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    def get_by_category(self, db: Session, *, category: str) -> Optional[Category]:
        return db.query(Category).filter(Category.category == category).first()

    def create(self, db: Session, *, obj_in: CategoryCreate) -> Category:
        db_obj = Category(
            category=obj_in.category,
            date=obj_in.date,
            controller=obj_in.controller,
            brand=obj_in.brand,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Category, obj_in: Union[CategoryUpdate, Dict[str, Any]]
    ) -> Category:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        # if update_data["password"]:
        #     hashed_password = get_password_hash(update_data["password"])
        #     del update_data["password"]
        #     update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Category]:
        return (
            db.query(self.model)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, db: Session, *, id: int) -> Optional[Category]:
        return db.query(Category).filter(Category.id == id).first()


category = CRUDCategory(Category)


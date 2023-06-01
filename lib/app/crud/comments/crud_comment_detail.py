from typing import Any, Dict, Optional, Union, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from lib.app.crud.base import CRUDBase
from lib.app.models.comments import CommentDetail

from lib.app.schemas.comments.comment_detail import CommentDetailCreate, CommentDetailUpdate


class CRUDCommentDetail(CRUDBase[CommentDetail, CommentDetailCreate, CommentDetailUpdate]):

    def create_with_owner(
            self, db: Session, *, obj_in: CommentDetailCreate
    ) -> CommentDetail:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create(
            self, db: Session, *, obj_in: CommentDetailCreate
    ) -> CommentDetail:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
            self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[CommentDetail]:
        return (
            db.query(self.model)
            .filter(CommentDetail.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[CommentDetail]:
        return (
            db.query(self.model)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, db: Session, *, comment_id: str) -> Any:
        return db.query(self.model).filter(CommentDetail.id == comment_id).first()

    def remove_by_id(self, db: Session, *, comment_id: str) -> Any:
        return super().remove_str_id(db, id=comment_id)

    def get_by_created_user_id(self, db: Session, *, created_user_id: str) -> Any:
        return db.query(self.model).filter(CommentDetail.created_user_id == created_user_id).first()

    # get by machine type
    def get_multi_by_service_status_id(
            self, db: Session, service_status_id: str, skip: int = 0, limit: int = 100
    ) -> List[CommentDetail]:
        return (
            db.query(self.model)
            .filter(CommentDetail.service_status_id == service_status_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get by machine manufacturer
    def get_multi_by_service_detail_id(
            self, db: Session, service_id: str, skip: int = 0, limit: int = 100
    ) -> List[CommentDetail]:
        return (
            db.query(self.model)
            .filter(CommentDetail.service_detail_id == service_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(
            self, db: Session, *, db_obj: CommentDetail, obj_in: Union[CommentDetailUpdate, Dict[str, Any]]
    ) -> CommentDetail:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)


comment_detail = CRUDCommentDetail(CommentDetail)

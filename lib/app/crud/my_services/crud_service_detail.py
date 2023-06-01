from typing import Any, Dict, Optional, Union, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from lib.app.crud.base import CRUDBase
from lib.app.models.my_services import ServiceDetail
from lib.app.schemas.my_services.service_detail import ServiceDetailCreate, ServiceDetailUpdate


class CRUDServiceDetail(CRUDBase[ServiceDetail, ServiceDetailCreate, ServiceDetailUpdate]):

    def create_with_owner(
        self, db: Session, *, obj_in: ServiceDetailCreate
    ) -> ServiceDetail:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create(
        self, db: Session, *, obj_in: ServiceDetailCreate
     ) -> ServiceDetail:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[ServiceDetail]:
        return (
            db.query(self.model)
            .filter(ServiceDetail.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ServiceDetail]:
        return (
            db.query(self.model)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, db: Session, *, id: str) -> Any:
        return db.query(self.model).filter(ServiceDetail.id == id).first()

    def get_by_created_user_id_service_type(self,
                                            db: Session,
                                            *,
                                            created_user_id: str,
                                            category_id: str
                                            ) -> Any:
        return (
            db.query(self.model)
            .filter(ServiceDetail.created_user_id == created_user_id)
            .filter(ServiceDetail.category_id == category_id)
            .all()
        )

    def get_by_service_id(self, db: Session, *, service_id: str) -> Optional[ServiceDetail]:
        return db.query(self.model).filter(ServiceDetail.id == service_id).first()

    #get by field
    def get_multi_by_company_name(
            self, db: Session, id: str, skip: int = 0, limit: int = 100
    ) -> List[ServiceDetail]:
        return (
            db.query(self.model)
            .filter(ServiceDetail.company_name == id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get by machine type
    def get_multi_by_machine_type(
            self, db: Session, machine_type: str, skip: int = 0, limit: int = 100
    ) -> List[ServiceDetail]:
        return (
            db.query(self.model)
            .filter(ServiceDetail.machine_type == machine_type)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get by machine manufacturer
    def get_multi_by_machine_manufacturer(
            self, db: Session, machine_manufacturer: str, skip: int = 0, limit: int = 100
    ) -> List[ServiceDetail]:
        return (
            db.query(self.model)
            .filter(ServiceDetail.machine_oem == machine_manufacturer)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get by category
    def get_multi_by_category(
            self, db: Session, id: int, skip: int = 0, limit: int = 100
    ) -> List[ServiceDetail]:
        return (
            db.query(self.model)
            .filter(ServiceDetail.category_id == id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get by category & company profile id
    def get_by_category_comp_profile(
            self, db: Session, category_id: str, company_profile_id: str, skip: int = 0, limit: int = 100
    ) -> List[ServiceDetail]:
        return (
            db.query(self.model)
            .filter(ServiceDetail.company_profile_id == company_profile_id)
            .filter(ServiceDetail.category_id == category_id)
            .all()
        )

    def update(
            self, db: Session, *, db_obj: ServiceDetail, obj_in: Union[ServiceDetailUpdate, Dict[str, Any]]
    ) -> ServiceDetail:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)


service_detail = CRUDServiceDetail(ServiceDetail)

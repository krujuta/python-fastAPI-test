from typing import List, Optional, Union, List, Dict, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from lib.app.crud.base import CRUDBase
from lib.app.models.base_users import CompanyProfile
from lib.app.schemas.base_users.company_profile import CompanyProfileCreate, CompanyProfileUpdate


class CRUDCompanyProfile(CRUDBase[CompanyProfile, CompanyProfileCreate, CompanyProfileUpdate]):
    def create_with_owner(
            self, db: Session, *, obj_in: CompanyProfileCreate
    ) -> CompanyProfile:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create(self, db: Session, *, obj_in: CompanyProfileCreate) -> CompanyProfile:
        db_obj = CompanyProfile(
            company_name= obj_in.company_name,
            company_address=obj_in.company_address,
            phone_number=obj_in.phone_number,
            email=obj_in.email,
            description=obj_in.description,
            is_service_provider=obj_in.is_service_provider,
            is_machine_user=obj_in.is_machine_user,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
            self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[CompanyProfile]:
        return (
            db.query(self.model)
            .filter(CompanyProfile.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get user details by username
    def get_by_email(self, db: Session, *, email: str) -> Optional[CompanyProfile]:
        return db.query(CompanyProfile).filter(CompanyProfile.email == email).first()

    def update(
            self, db: Session, *, db_obj: CompanyProfile, obj_in: Union[CompanyProfileUpdate, Dict[str, Any]]
    ) -> CompanyProfile:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    #  get by user_id
    # def get_by_id(
    #         self, db: Session, id: int, skip: int = 0, limit: int = 100
    # ) -> List[CompanyProfile]:
    #     return (
    #         db.query(self.model)
    #         .filter(CompanyProfile.id == id)
    #         .offset(skip)
    #         .limit(limit)
    #         .all()
    #     )

    def get_by_id(self, db: Session, *, id: str) -> Optional[CompanyProfile]:
        return db.query(CompanyProfile).filter(CompanyProfile.id == id).first()

    def get_by_name(self, db: Session, *, company_name: str) -> Optional[CompanyProfile]:
        return db.query(CompanyProfile).filter(CompanyProfile.company_name == company_name).first()

    def remove_by_id(self, db: Session, *, company_id: str) -> Any:
        return super().remove_str_id(db, id=company_id)


company_profile = CRUDCompanyProfile(CompanyProfile)

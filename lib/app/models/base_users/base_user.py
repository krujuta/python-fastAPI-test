
from lib.app.db.base_class import Base
from sqlalchemy import Boolean, Column, Sequence, String, ForeignKey
from sqlalchemy.orm import relationship


class BaseUser(Base):
    TABLE_ID = Sequence('baseuser_seq_xxx')
    id = Column(String, primary_key=True, index=True, nullable=False, server_default=TABLE_ID.next_value())
    name = Column(String, index=True, nullable=False, default='')
    job_title = Column(String, index=True, nullable=False, default='')
    phone_number = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, index=True, unique=True)
    is_admin = Column(Boolean(), default=False)
    is_normal_user = Column(Boolean(), default=False)
    image_url = Column(String, default='')
    company_profile_id = Column(String, ForeignKey('companyprofile.id'))
    company_profile = relationship("CompanyProfile", foreign_keys="BaseUser.company_profile_id")
    is_service_provider = Column(Boolean(), default=False)
    is_machine_user = Column(Boolean(), default=False)
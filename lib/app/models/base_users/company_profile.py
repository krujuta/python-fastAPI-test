from lib.app.db.base_class import Base
from sqlalchemy import Boolean, Column, Integer, String, ARRAY, Sequence


class CompanyProfile(Base):
    TABLE_ID = Sequence('companyprofile_seq_xxx')
    id = Column(String, primary_key=True, index=True, nullable=False, server_default=TABLE_ID.next_value())
    company_name = Column(String, index=True, nullable=False, default='')
    company_address = Column(String, index=True, nullable=False, default='')
    phone_number = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    description = Column(String, default='')
    image_url = Column(String, default='')
    is_service_provider = Column(Boolean(), default=False)
    service_providers_list = Column(ARRAY(Integer), index=True)
    is_machine_user = Column(Boolean(), default=False)
    machine_users_list = Column(ARRAY(Integer), index=True)

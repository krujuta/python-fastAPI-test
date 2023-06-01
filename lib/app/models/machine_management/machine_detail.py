from lib.app.db.base_class import Base
from sqlalchemy import Column, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship


class MachineDetail(Base):
    TABLE_ID = Sequence('machinedetail_seq_xxx')
    id = Column(String, primary_key=True, index=True, nullable=False, server_default=TABLE_ID.next_value())
    machine = Column(String, index=True, nullable=False)

    machine_type_id = Column(String, ForeignKey('machinetype.id'))
    construction_year = Column(String, index=True, default='None')
    created_user_id = Column(String, ForeignKey('baseuser.id'))
    company_profile_id = Column(String, ForeignKey('companyprofile.id'))
    machine_type = Column(String, index=True, nullable=False)
    created_user_profile = relationship("BaseUser", foreign_keys="MachineDetail.created_user_id")
    company_profile = relationship("CompanyProfile", foreign_keys="MachineDetail.company_profile_id")

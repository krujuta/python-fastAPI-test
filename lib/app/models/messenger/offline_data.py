from lib.app.db.base_class import Base
from typing import TYPE_CHECKING
from sqlalchemy import Column, ForeignKey, Integer, String

if TYPE_CHECKING:
    from lib.app.models.base_users.base_user import BaseUser  # noqa: F401


class OfflineData(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    company = Column(String, index=True, default='')  # (offering name / company name)
    sender_id = Column(String)
    receiver_id = Column(String)
    content = Column(String, index=True, default='')
    date = Column(String, index=True, default='')  # server time when data is pushed in db
    content_type = Column(String, index=True, default='')  # content type - will be used in future to store different types of data.

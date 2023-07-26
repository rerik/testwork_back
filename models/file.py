from sqlalchemy import Column, Integer, String, DateTime
from database import Base


class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    extension = Column(String)
    size = Column(Integer)
    path = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    comment = Column(String)

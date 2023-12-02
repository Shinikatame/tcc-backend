from sqlalchemy import Column, Integer, String, Boolean
from database import Base

from models.support import Support

class SupportORM(Base):
    __tablename__ = 'support'
    
    id = Column(Integer, primary_key=True, index=True)
    name_student = Column(String)
    name_responsible = Column(String)
    email_responsible = Column(String)
    description = Column(String)
    status = Column(String)
    date = Column(Integer)
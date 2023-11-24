from sqlalchemy import Column, Integer, String, Boolean
from database import Base, commit, engine, AsyncSessionLocal

from models.user import UserSignUp
from models.classes import Class

class ClassesORM(Base):
    __tablename__ = 'classes'
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer)
    name = Column(String)
    description = Column(String)
    link = Column(String)
    order = Column(Integer)
    
    @classmethod
    @commit
    async def create_class(cls, class_: Class):
        return cls(**class_.dict())
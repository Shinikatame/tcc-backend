from sqlalchemy import Column, Integer, String, Boolean
from database import Base

from models.courses import Courses

class CoursesORM(Base):
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    image = Column(String)
    actived = Column(Boolean)

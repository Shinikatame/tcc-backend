from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class QuestionsORM(Base):
    __tablename__ = 'questions'
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer)
    statement = Column(String)
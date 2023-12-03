from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class QuestionsAnswersORM(Base):
    __tablename__ = 'questions_answers'
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer)
    option = Column(String)
    correct = Column(Boolean)
    order = Column(Integer)
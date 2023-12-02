from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class MaterialORM(Base):
    __tablename__ = 'complementary_material'
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer)
    file = Column(String)
from sqlalchemy import Column, Integer, String, Boolean
from database import Base

from models.user import UserSignUp

class UserORM(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique = True)
    password = Column(String)
    birth = Column(Integer)
    name_responsible = Column(String)
    email_responsible = Column(String)
    cpf_responsible = Column(String)
    zip_code = Column(String)
    city = Column(String)
    address = Column(String)
    state = Column(String)
    scholarship_holder = Column(Boolean)
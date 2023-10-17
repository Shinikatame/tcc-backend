from sqlalchemy import Column, Integer, String, Boolean
from database import Base, commit, engine, AsyncSessionLocal

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

    def __repr__(self) -> str:
        return f'UserORM(id={self.id}, name={self.name}, email={self.email}, password={self.password}, birth={self.birth}, name_responsible={self.name_responsible}, email_responsible={self.email_responsible}, cpf_responsible={self.cpf_responsible}, zip_code={self.zip_code}, city={self.city}, address={self.address}, state={self.state}, scholarship_holder={self.scholarship_holder})'

    @classmethod
    @commit
    async def create_user(cls, user: UserSignUp):
        return cls(**user.dict())
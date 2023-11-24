from sqlalchemy import Column, Integer, String, Boolean
from database import Base, commit, engine, AsyncSessionLocal

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

    def __repr__(self) -> str:
        return f'UserORM(id={self.id}, name={self.name}, email={self.email}, password={self.password}, birth={self.birth}, name_responsible={self.name_responsible}, email_responsible={self.email_responsible}, cpf_responsible={self.cpf_responsible}, zip_code={self.zip_code}, city={self.city}, address={self.address}, state={self.state}, scholarship_holder={self.scholarship_holder})'

    @classmethod
    @commit
    async def create_support(cls, support: Support):
        return cls(**support.dict())
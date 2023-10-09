from sqlalchemy import Column, Integer, String
from database import Base, commit, engine, AsyncSessionLocal

from models.user import UserSignUp

class UserORM(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique = True)
    email = Column(String, unique = True)
    password = Column(String)

    def __repr__(self) -> str:
        return f'UserORM(id={self.id}, name={self.username}, email={self.email}, password={self.password})'

    @classmethod
    @commit
    async def create_user(cls, user: UserSignUp):
        return cls(**user.dict())
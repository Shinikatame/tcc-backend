from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from ssl import create_default_context
from dotenv import load_dotenv
from os import getenv

load_dotenv()

USERNAME = getenv('DATABASE_USERNAME')
PASSWORD = getenv('DATABASE_PASSWORD')
HOST = getenv('DATABASE_HOST')
NAME = getenv('DATABASE')

SQL_URL =  f'mysql+aiomysql://{USERNAME}:{PASSWORD}@{HOST}/{NAME}'

ctx = create_default_context(cafile = '/etc/ssl/certs/ca-certificates.crt')
engine = create_async_engine(
    SQL_URL, 
    connect_args = {'ssl': ctx},
    pool_pre_ping = True, 
    echo = True
)

AsyncSessionLocal = sessionmaker(engine, expire_on_commit = False, class_ = AsyncSession)

class Base(DeclarativeBase):
    def dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    
    @classmethod
    async def find_one(cls, **filter):
        async with AsyncSessionLocal() as db:
            stmt = select(cls).filter_by(**filter)
            result = await db.execute(stmt)
            return result.scalars().first()
        
    @classmethod
    async def find_many(cls, **filter):
        async with AsyncSessionLocal() as db:
            stmt = select(cls).filter_by(**filter)
            result = await db.execute(stmt)
            return result.scalars().all()
     
        
def commit(coro):
    async def wrapper(*args, **kwargs):
        async with AsyncSessionLocal() as db:
            query = await coro(*args, **kwargs)
            db.add(query)
            await db.commit()
        
    return wrapper
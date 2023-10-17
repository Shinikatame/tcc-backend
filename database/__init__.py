from sqlalchemy import update, delete, and_, text
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from ssl import create_default_context
from dotenv import load_dotenv
from os import getenv

load_dotenv()

SSL = getenv('SSL')
PROTOCOL = getenv('PROTOCOL')
CONNECTOR = getenv('CONNECTOR_ASYNC')
PROTOCOL = getenv('PROTOCOL')
USERNAME = getenv('DB_USERNAME')
PASSWORD = getenv('DB_PASSWORD')
HOST = getenv('DB_HOST')
DB = getenv('DB_NAME')

SQL_URL =  f'{PROTOCOL}{CONNECTOR}://'

if USERNAME and PASSWORD: SQL_URL += f'{USERNAME}:{PASSWORD}@'

SQL_URL += f'{HOST}'

if DB: SQL_URL += f'/{DB}'

connect_args = {}

if SSL:
    connect_args['ssl'] =  create_default_context(cafile = SSL)

engine = create_async_engine(
    SQL_URL, 
    connect_args = connect_args,
    pool_pre_ping = True, 
    echo = True
)

AsyncSessionLocal = sessionmaker(engine, expire_on_commit = False, class_ = AsyncSession)

class Base(DeclarativeBase):
    def dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    
    @classmethod
    async def update(cls, id: int, **kwargs):
        async with AsyncSessionLocal() as db:
            stmt = update(cls).where(getattr(cls, 'id') == id).values(**kwargs)
            result = await db.execute(stmt)
            await db.commit()
            
            if result.rowcount != 0:
                data = await cls.find_one(id = id)
                return data
    
    @classmethod
    async def delete(cls, **kwargs):
        async with AsyncSessionLocal() as db:
            stmt = delete(cls).where(and_(*[getattr(cls, col) == value for col, value in kwargs.items()]))
            result = await db.execute(stmt)
            await db.commit()
            return result.rowcount != 0
            
    @classmethod
    async def find_one(cls, **kwargs):
        async with AsyncSessionLocal() as db:
            stmt = select(cls).filter_by(**kwargs)
            result = await db.execute(stmt)
            return result.scalars().first()
        
    @classmethod
    async def find_many(cls, **kwargs):
        async with AsyncSessionLocal() as db:
            stmt = select(cls).filter_by(**kwargs)
            result = await db.execute(stmt)
            return result.scalars().all()
        
    @classmethod    
    async def find_many_regex(cls, **kwargs):
        async with AsyncSessionLocal() as db:
            col, re = list(kwargs.items())[0]
            
            stmt = select(cls).filter(text(f'{col} REGEXP "{re}"'))
            result = await db.execute(stmt)
            return result.scalars().all()
        
def commit(coro):
    async def wrapper(*args, **kwargs):
        async with AsyncSessionLocal() as db:
            query = await coro(*args, **kwargs)
            db.add(query)
            await db.commit()
            await db.refresh(query)
            return query
    return wrapper
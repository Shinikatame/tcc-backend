from jwt import encode
from passlib.context import CryptContext

from dotenv import load_dotenv
from os import getenv

load_dotenv()
password_hash = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_jwt(user_email: str):
    data = {"sub": user_email}
    token = encode(data, getenv('SECRET_KEY'), algorithm=getenv('ALGORITHM'))
    return token
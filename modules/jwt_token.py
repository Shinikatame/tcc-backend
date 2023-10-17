from fastapi import HTTPException, status
from jwt import encode, decode
from jwt.exceptions import DecodeError
from passlib.context import CryptContext

from models.user import UserToken, UserSignUp, UserResponse
from database.auth import UserORM

from dotenv import load_dotenv
from os import getenv

load_dotenv()

SECRET_KEY = getenv('SECRET_KEY')
ALGORITHM = getenv('ALGORITHM')

password_hash = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_jwt(user: UserSignUp) -> str:
    data = UserToken(**user.dict())
    token = encode(data.dict(), SECRET_KEY, algorithm = ALGORITHM)
    return token

async def verify_jwt(token: str) -> UserResponse:
    try:
        payload = decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        decoded = UserToken(**payload, token = token)
        user = await UserORM.find_one(id = decoded.id)
        response = UserResponse(**user.dict(), token = token)
        return response
    
    except DecodeError: raise HTTPException(status_code = 401, detail = "Token JWT inválido")
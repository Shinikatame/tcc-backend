from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import encode, decode
from jwt.exceptions import DecodeError
from passlib.context import CryptContext

from models.user import UserToken, UserSignUp, UserResponse
from database.user import UserORM

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
    

async def has_authenticated(auth: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> UserToken:
    try:
        token = auth.credentials
        user = decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        return UserToken(**user, token = token)
    
    except Exception: raise HTTPException(status_code = 401, detail = "Token JWT inválido")

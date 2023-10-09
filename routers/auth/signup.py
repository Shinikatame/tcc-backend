from fastapi import APIRouter, HTTPException, status

from models.user import UserCreate, User
from database.auth import auth
from modules.jwt_token import create_jwt, password_hash

router = APIRouter()

@router.post("/signup", response_model = User)
async def cadastrar_usuario(user: UserCreate):
    if any(existing_user['email'] == user.email for existing_user in auth.data):
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "O email já está em uso")

    user.password = password_hash.hash(user.password)
    auth.create(user)
    
    token = create_jwt(user.email)
    response = User(**user.dict(), token = token)
    
    return response

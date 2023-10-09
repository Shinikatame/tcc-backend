from fastapi import APIRouter, HTTPException, status

from models.user import UserLogin, User
from database.auth import auth
from modules.jwt_token import create_jwt, password_hash

router = APIRouter()

@router.post("/signin", response_model = User)
async def login(params: UserLogin):
    user = next((u for u in auth.data if u['email'] == params.email), None)
    
    if not user or not password_hash.verify(params.password, user['password']):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Credenciais inválidas")
    
    token = create_jwt(user['email'])
    response = User(**user, token = token)
    return response

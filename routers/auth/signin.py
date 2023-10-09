from fastapi import APIRouter, HTTPException, status

from models.user import UserSignIn, UserResponse
from database.auth import UserORM
from modules.jwt_token import create_jwt, password_hash

router = APIRouter()

@router.post("/signin", response_model = UserResponse)
async def signin(body: UserSignIn):
    user = await UserORM.find_one(email = body.email)
    if not user or not password_hash.verify(body.password, user.password): 
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Credenciais inválidas")
    
    token = create_jwt(user.email)
    response = UserResponse(**user.dict(), token = token)
    return response

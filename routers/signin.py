from fastapi import HTTPException, status
from routers import router

from models.user import UserSignIn, UserResponse
from database.auth import UserORM
from modules.jwt_token import create_jwt, password_hash

@router.post("/signin", status_code = 201, response_model = UserResponse)
async def signin(body: UserSignIn):
    user = await UserORM.find_one(email = body.email)
    
    if not user or not password_hash.verify(body.password, user.password): 
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Credenciais inválidas")
    
    token = create_jwt(user)
    response = UserResponse(**user.dict(), token = token)
    return response

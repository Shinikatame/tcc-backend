from fastapi import HTTPException, status
from routers import router

from models.user import UserSignUp, UserResponse
from database.auth import UserORM
from modules.jwt_token import create_jwt, password_hash

@router.post("/signup", status_code = 201, response_model = UserResponse)
async def signup(body: UserSignUp):
    user = await UserORM.find_one(email = body.email)
    if user:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "O email já está em uso")

    body.password = password_hash.hash(body.password)
    data = await UserORM.create_user(body)
        
    token = create_jwt(data)
    response = UserResponse(**data.dict(), token = token)
    return response

from fastapi import HTTPException, status, Header
from routers import router

from models.user import UserEdit, UserResponse
from database.auth import UserORM
from modules.jwt_token import verify_jwt

@router.get("/profile", response_model = UserResponse)
async def profile_get(Authorization: str = Header(None)):
    if not Authorization or not Authorization.startswith("Bearer "):
        detail = 'Cabeçalho "Authorization" não especificado na solicitação' if not Authorization else 'Token JWT inválido'
        raise HTTPException(status_code = 401, detail = detail)
    
    token = Authorization.replace('Bearer ', '')
    user = await verify_jwt(token)
    response = UserResponse(**user.dict())
     
    return response


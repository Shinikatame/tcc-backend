from fastapi import HTTPException, status, Depends, Header
from routers import router

from models.user import UserSignUp, UserSignIn, UserEdit, UserResponse
from database.user import UserORM
from modules.jwt_token import create_jwt, password_hash, has_authenticated

@router.post("/signup", status_code = 201, response_model = UserResponse)
async def signup(params: UserSignUp):
    user = await UserORM.find_one(email = params.email)
    if user:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "O email já está em uso")

    if len(params.state) >= 3:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "String 'state' aceita no max 2 caracteres")
    
    params.password = password_hash.hash(params.password)
    data = await UserORM.create(**params.dict())
        
    token = create_jwt(data)
    response = UserResponse(**data.dict(), token = token)
    return response


@router.post("/signin", status_code = 201, response_model = UserResponse)
async def signin(params: UserSignIn):
    user = await UserORM.find_one(email = params.email)
    
    if not user or not password_hash.verify(params.password, user.password): 
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Credenciais inválidas")

    token = create_jwt(user)
    response = UserResponse(**user.dict(), token = token)
    return response


@router.get("/profile", response_model = UserResponse)
async def profile_get(Authorization: str = Header(None)):
    if not Authorization or not Authorization.startswith("Bearer "):
        detail = 'Cabeçalho "Authorization" não especificado na solicitação' if not Authorization else 'Token JWT inválido'
        raise HTTPException(status_code = 401, detail = detail)
    
    token = Authorization.replace('Bearer ', '')
    user = await verify_jwt(token)
    response = UserResponse(**user.dict())
     
    return response


@router.put("/profile", response_model = UserResponse)
async def profile_edit(user_update: UserEdit, user: dict = Depends(has_authenticated)):
    user = await UserORM.update(user.id, **user_update.dict())
    response = UserResponse(**user.dict())
     
    return response

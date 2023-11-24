from fastapi import HTTPException, status 
from routers.admin import router

from typing import List

from models.user import UserSignUp, UserEdit, UserResponse
from database.auth import UserORM

from modules.jwt_token import create_jwt, password_hash

@router.get("/students/{student_id}", response_model = UserResponse)
async def student_get(student_id: int):
    user = await UserORM.find_one(id = student_id)
    if not user:
        raise HTTPException(status_code = 404, detail = 'Aluno não encontrado')

    response = UserResponse(**user.dict())
    return response


@router.post("/students", status_code = 201, response_model = UserResponse)
async def student_create(body: UserSignUp):
    user = await UserORM.find_one(email = body.email)    
    if user:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "O email já está em uso")
    
    body.password = password_hash.hash(body.password)
    data = await UserORM.create_user(body)
        
    token = create_jwt(data)
    response = UserResponse(**data.dict(), token = token)
    return response


@router.put("/students/{student_id}", response_model = UserResponse)
async def student_edit(student_id: int, user_update: UserEdit):
    user = await UserORM.update(student_id, **user_update.dict())
    if not user:
        raise HTTPException(status_code = 404, detail = 'Aluno não encontrado')

    response = UserResponse(**user.dict())
    return response


@router.delete("/students/{student_id}", status_code = 204)
async def student_delete(student_id: int):
    response = await UserORM.delete(id = student_id)
    if not response:
        raise HTTPException(status_code = 404, detail = 'Aluno não encontrado')


@router.get("/students", response_model = List[UserResponse])
async def students():
    students = await UserORM.find_many()
    response = [UserResponse(**s.dict()) for s in students if isinstance(s.dict(), dict)]
    return response


@router.get("/students/regex/{regex}", response_model = List[UserResponse])
async def students_search(regex: str):
    students = await UserORM.find_many_regex(name = regex)
    response = [UserResponse(**s.dict()) for s in students if isinstance(s.dict(), dict)]
    return response

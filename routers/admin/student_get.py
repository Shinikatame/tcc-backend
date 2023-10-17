from fastapi import HTTPException, status
from routers.admin import router

from models.user import UserEdit, UserResponse
from database.auth import UserORM

@router.get("/students/{student_id}", response_model = UserResponse)
async def student_get(student_id: int):
    user = await UserORM.find_one(id = student_id)
    if not user:
        raise HTTPException(status_code = 404, detail = 'Aluno não encontrado')

    response = UserResponse(**user.dict())
    return response


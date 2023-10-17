from fastapi import HTTPException, status
from routers.admin import router

from models.user import UserEdit, UserResponse
from database.auth import UserORM

@router.put("/students/{student_id}", response_model = UserResponse)
async def student_edit(student_id: int, user_update: UserEdit):
    user = await UserORM.update(student_id, **user_update.dict())
    if not user:
        raise HTTPException(status_code = 404, detail = 'Aluno não encontrado')

    response = UserResponse(**user.dict())
    return response


from fastapi import HTTPException, status
from routers.admin import router

from database.auth import UserORM

@router.delete("/students/{student_id}", status_code = 204)
async def student_delete(student_id: int):
    response = await UserORM.delete(id = student_id)
    if not response:
        raise HTTPException(status_code = 404, detail = 'Aluno não encontrado')


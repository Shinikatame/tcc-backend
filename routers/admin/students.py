from routers.admin import router

from typing import List

from models.user import UserResponse
from database.auth import UserORM

@router.get("/students", response_model = List[UserResponse])
async def students():
    students = await UserORM.find_many()
    response = [UserResponse(**s.dict()) for s in students if isinstance(s.dict(), dict)]
    return response

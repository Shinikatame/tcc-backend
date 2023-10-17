from routers.admin import router

from typing import List

from models.user import UserResponse
from database.auth import UserORM

@router.get("/students/regex/{regex}", response_model = List[UserResponse])
async def students_search(regex: str):
    students = await UserORM.find_many_regex(name = regex)
    response = [UserResponse(**s.dict()) for s in students if isinstance(s.dict(), dict)]
    return response

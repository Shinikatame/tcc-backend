from fastapi import HTTPException, status 
from routers.admin import router

from typing import List

from models.painels import DashboardResponse, FinancialResponse
from database.user import UserORM
from database.support import SupportORM

@router.get("/dashboard", response_model = DashboardResponse)
async def dashboard():
    students = await UserORM.find_many()
    scholarship_holder = [s for s in students if s.scholarship_holder]
    supports = await SupportORM.find_many()

    response = DashboardResponse(students = len(students), scholarship_holder = len(scholarship_holder), supports = len(supports))
    return response


@router.get("/financial", response_model = FinancialResponse)
async def financial():
    students = await UserORM.find_many()

    students_paying = [s for s in students if not s.scholarship_holder]
    students_scholarship = [s for s in students if s.scholarship_holder]

    response = FinancialResponse(students_paying = len(students_paying), students_scholarship = len(students_scholarship))
    return response
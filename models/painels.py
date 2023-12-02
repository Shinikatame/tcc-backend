from pydantic import BaseModel


class DashboardResponse(BaseModel):
    students: int
    scholarship_holder: int
    supports: int


class FinancialResponse(BaseModel):
    students_paying: int
    students_scholarship: int
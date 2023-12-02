from pydantic import BaseModel

class DashboardResponse(BaseModel):
    students: int
    scholarship_holder: int
    supports: int
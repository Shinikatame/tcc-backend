from pydantic import BaseModel
    
class Classes(BaseModel):
    name: str
    description: str
    link: str


class Class(Classes):
    course_id: int
    

class ClassesResponse(Classes):
    id: int
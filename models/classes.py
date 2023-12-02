from pydantic import BaseModel

from typing import List, Optional
    
class Classes(BaseModel):
    name: str
    description: str
    link: str


class Class(Classes):
    course_id: int
    order: int
    

class ClassesResponse(Classes):
    id: int


class ClassesLink(BaseModel):
    id: int
    name: str
    link: str


class ClassCurrent(BaseModel):
    current: ClassesResponse
    next_classes: List[ClassesLink]
    material: Optional[str] = None
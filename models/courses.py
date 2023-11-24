from pydantic import BaseModel
from typing import List

from models.classes import ClassesResponse, Classes
    
class Courses(BaseModel):
    name: str
    image: str


class CoursesPost(Courses):
    classes: List[Classes]


class CourseResponse(Courses):
    id: int


class CoursesResponse(Courses):
    id: int
    classes: List[ClassesResponse]
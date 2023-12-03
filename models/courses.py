from pydantic import BaseModel
from typing import List, Optional

from models.classes import ClassesResponse, Classes
    
class Courses(BaseModel):
    name: str
    image: str
    actived: Optional[bool] = True


class CoursesPost(Courses):
    classes: List[Classes]


class CourseResponse(Courses):
    id: int
    class_id: int

class CoursesResponse(Courses):
    id: int
    classes: List[ClassesResponse]
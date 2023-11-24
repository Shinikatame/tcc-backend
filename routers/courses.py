from fastapi import HTTPException, status, Header
from routers import router

from typing import List

from models.courses import CourseResponse
from models.classes import ClassCurrent
from database.courses import CoursesORM
from database.classes import ClassesORM


@router.get("/courses", status_code = 200, response_model = List[CourseResponse])
async def courses_get():
    courses = await CoursesORM.find_many()
    response = [CourseResponse(**c.dict()) for c in courses if isinstance(c.dict(), dict)]
    return response



@router.get("/courses/{course_id}/class/{class_id}", status_code = 200, response_model = ClassCurrent)
async def classe_get(course_id: int, class_id: int):
    class_ = await ClassesORM.find_one(id = class_id)
    if class_.course_id != course_id:
        raise HTTPException(status_code = 404, detail = 'Aulas não encontradas')

    classes = await ClassesORM.find_many(course_id = course_id)
    
    next_classes = [c.dict() for c in classes if isinstance(c.dict(), dict)]
    next_classes = sorted(next_classes, key = lambda c: c.get('order'))
    
    response = ClassCurrent(
        current = class_.dict(), 
        next_classes = next_classes[class_.order+1:]
    )
    
    return response
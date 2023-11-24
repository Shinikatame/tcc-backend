from fastapi import HTTPException, status 
from routers.admin import router

from asyncio import create_task, gather

from models.courses import CoursesPost, CoursesResponse, Courses
from models.classes import Classes, Class
from database.courses import CoursesORM
from database.classes import ClassesORM


async def create_class(index: int, course_id: int, class_: Classes):
    data = await ClassesORM.create_class(Class(order = index, course_id = course_id, **class_.dict()))
    return data


@router.post("/courses", status_code = 201, response_model = CoursesResponse)
async def student_create(parms: CoursesPost):
    course = await CoursesORM.create_course(Courses(**parms.dict()))

    classes = [create_task(create_class(i, course.id, c)) for i, c in enumerate(parms.classes)]
    results = await gather(*classes)

    classes = [c.dict() for c in results]

    response = CoursesResponse(classes = classes, **course.dict())
    return response

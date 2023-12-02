from fastapi import HTTPException, status 
from routers.admin import router

from asyncio import create_task, gather

from models.courses import CoursesPost, CoursesResponse, Courses
from models.classes import Classes, Class
from models.material import Material, MaterialResponse
from database.courses import CoursesORM
from database.classes import ClassesORM
from database.material import MaterialORM


async def create_class(index: int, course_id: int, class_: Classes):
    data = await ClassesORM.create(**Class(order = index, course_id = course_id, **class_.dict()).dict())
    return data


@router.post("/courses", status_code = 201, response_model = CoursesResponse)
async def course_create(parms: CoursesPost):
    course = await CoursesORM.create(**Courses(**parms.dict()).dict())

    classes = [create_task(create_class(i, course.id, c)) for i, c in enumerate(parms.classes)]
    results = await gather(*classes)

    classes = [c.dict() for c in results]

    response = CoursesResponse(classes = classes, **course.dict())
    return response


@router.post("/courses/{course_id}/material", status_code = 201, response_model = MaterialResponse)
async def material_create(course_id: int, params: Material):
    material = await MaterialORM.create(course_id = course_id, file = params.file)
    response = MaterialResponse(**material.dict())
    return response

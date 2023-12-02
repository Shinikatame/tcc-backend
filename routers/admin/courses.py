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


@router.put("/courses/{course_id}", status_code = 201, response_model = CoursesResponse)
async def course_edit(course_id: int, parms: CoursesPost):
    course = await CoursesORM.update(course_id, **Courses(**parms.dict()).dict())

    classes = [create_task(create_class(i, course.id, c)) for i, c in enumerate(parms.classes)]
    results = await gather(*classes)

    classes = [c.dict() for c in results]

    response = CoursesResponse(classes = classes, **course.dict())
    return response


@router.delete("/courses/{course_id}", status_code = 204)
async def course_delete(course_id: int):
    course = await CoursesORM.delete(id = course_id)
    if not course: raise HTTPException(status_code = 404, detail = 'Curso não encontrado')
    await ClassesORM.delete(course_id = course_id)
    await MaterialORM.delete(course_id = course_id)


@router.delete("/courses/{course_id}/classe/{class_id}", status_code = 204)
async def class_delete(course_id: int, class_id: int):
    class_ = await ClassesORM.delete(id = class_id, course_id = course_id)
    if not class_: raise HTTPException(status_code = 404, detail = 'Aula não encontrada')


@router.get("/courses/{course_id}/material", status_code = 200, response_model = MaterialResponse)
async def material(course_id: int):
    material = await MaterialORM.find_one(course_id = course_id)
    if not material: raise HTTPException(status_code = 404, detail = 'Material não encontrado')
    response = MaterialResponse(**material.dict())
    return response


@router.post("/courses/{course_id}/material", status_code = 201, response_model = MaterialResponse)
async def material_create(course_id: int, params: Material):
    material = await MaterialORM.create(course_id = course_id, file = params.file)
    response = MaterialResponse(**material.dict())
    return response


@router.put("/courses/{course_id}/material/{material_id}", status_code = 201, response_model = MaterialResponse)
async def material_edit(course_id: int, material_id: int, params: Material):
    material = await MaterialORM.update(material_id, file = params.file)
    response = MaterialResponse(**material.dict())
    return response


@router.delete("/courses/{course_id}/material/{material_id}", status_code = 204)
async def material_delete(course_id: int, material_id: int):
    material = await MaterialORM.delete(id = material_id, course_id = course_id)
    if not material: raise HTTPException(status_code = 404, detail = 'Material não encontrado')
from fastapi import HTTPException, status 
from routers.admin import router

from asyncio import create_task, gather

from models.courses import CourseResponse, CoursesPost, CoursesResponse, Courses
from models.classes import Classes, Class, ClassesResponse
from models.material import Material, MaterialResponse
from models.questions import Question, QuestionPut, QuestionAnswers, QuestionAnswersResponse, QuestionResponse
from database.courses import CoursesORM
from database.classes import ClassesORM
from database.material import MaterialORM
from database.questions import QuestionsORM
from database.questions_answers import QuestionsAnswersORM

from typing import List

async def create_class(index: int, course_id: int, class_: Classes):
    data = await ClassesORM.create(**Class(order = index, course_id = course_id, **class_.dict()).dict())
    return data.dict()


async def add_answers(index: int, question_id: int, answers: QuestionAnswers):
    data = await QuestionsAnswersORM.create(question_id = question_id, order = index, **answers.dict())
    return QuestionAnswersResponse(**data.dict())


@router.post("/courses", status_code = 201, response_model = CoursesResponse)
async def course_create(parms: CoursesPost):
    course = await CoursesORM.create(**Courses(**parms.dict()).dict())

    classes = [create_task(create_class(i, course.id, c)) for i, c in enumerate(parms.classes)]
    results = await gather(*classes)

    response = CoursesResponse(classes = classes, **course.dict())
    return response





@router.get("/courses/{course_id}", status_code = 200, response_model = CoursesResponse)
async def course_get(course_id: int):
    course = await CoursesORM.find_one(id = course_id)
    if not course: raise HTTPException(status_code = 404, detail = 'Curso não encontrado')

    classes = await ClassesORM.find_many(course_id = course_id)
    classes = [ClassesResponse(**c.dict()) for c in classes]

    response = CoursesResponse(classes = classes, **course.dict())
    return response


@router.put("/courses/{course_id}", status_code = 201, response_model = CoursesResponse)
async def course_edit(course_id: int, parms: CoursesPost):
    course = await CoursesORM.update(course_id, **Courses(**parms.dict()).dict())

    classes = [create_task(create_class(i, course.id, c)) for i, c in enumerate(parms.classes)]
    results = await gather(*classes)

    response = CoursesResponse(classes = classes, **course.dict())
    return response


@router.delete("/courses/{course_id}", status_code = 204)
async def course_delete(course_id: int):
    course = await CoursesORM.delete(id = course_id)
    if not course: raise HTTPException(status_code = 404, detail = 'Curso não encontrado')
    await ClassesORM.delete(course_id = course_id)
    await MaterialORM.delete(course_id = course_id)

    await QuestionsORM.delete(course_id = course_id)
    for question in questions:
        await QuestionsAnswersORM.delete(question_id = question.id)


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


@router.put("/courses/{course_id}/material", status_code = 201, response_model = MaterialResponse)
async def material_edit(course_id: int, params: Material):
    course = await CoursesORM.find_one(id = course_id)
    if not course: raise HTTPException(status_code = 404, detail = 'Curso não encontrado')

    material = await MaterialORM.find_one(course_id = course_id)
    if not material: raise HTTPException(status_code = 404, detail = 'Curso não possui material')

    material = await MaterialORM.update(material.id, file = params.file)
    response = MaterialResponse(**material.dict())
    return response


@router.delete("/courses/{course_id}/material", status_code = 204)
async def material_delete(course_id: int):
    material = await MaterialORM.delete(course_id = course_id)
    if not material: raise HTTPException(status_code = 404, detail = 'Material não encontrado')





@router.get("/courses/{course_id}/questions", status_code = 200, response_model = List[QuestionResponse])
async def question_get(course_id: int):
    course = await CoursesORM.find_one(id = course_id)
    if not course: raise HTTPException(status_code = 404, detail = 'Curso não encontrado')

    response = []
    questions = await QuestionsORM.find_many(course_id = course_id)
    
    for question in questions:
        answers = await QuestionsAnswersORM.find_many(question_id = question.id)
        answers = [QuestionAnswersResponse(**a.dict()) for a in answers]

        data = QuestionResponse(**question.dict())
        data.answers = [QuestionAnswersResponse(**a.dict()) for a in answers]

        response.append(data)

    return response


@router.post("/courses/{course_id}/questions", status_code = 201, response_model = List[QuestionResponse])
async def question_create(course_id: int, questions: List[Question]):
    course = await CoursesORM.find_one(id = course_id)
    if not course: raise HTTPException(status_code = 404, detail = 'Curso não encontrado')

    response = []
    
    for qt in questions:
        question = await QuestionsORM.create(course_id = course_id, statement = qt.statement)
        answers = [create_task(add_answers(i, question.id, q)) for i, q in enumerate(qt.answers)]
        answers_results = await gather(*answers)

        data = QuestionResponse(**question.dict())
        data.answers.append(answers_results)
        response.append(data)

    return response


@router.put("/courses/{course_id}/questions", status_code = 201, response_model = List[QuestionResponse])
async def question_edit(course_id: int, questions: List[QuestionPut]):
    course = await CoursesORM.find_one(id = course_id)
    if not course: raise HTTPException(status_code = 404, detail = 'Curso não encontrado')


    couse_questions = await QuestionsORM.find_many(course_id = course_id)
    if not couse_questions: raise HTTPException(status_code = 404, detail = 'Curso não possui questões')
   
    response = []
    
    for qt in questions:
        question = await QuestionsORM.update(qt.id, statement = qt.statement)
        await QuestionsAnswersORM.delete(question_id = qt.id)
        answers = [create_task(add_answers(i, question.id, q)) for i, q in enumerate(qt.answers)]
        answers_results = await gather(*answers)

        data = QuestionResponse(**question.dict())
        data.answers.append(answers_results)
        response.append(data)

    return response


@router.delete("/courses/{course_id}/questions", status_code = 204)
async def question_delete(course_id: int):
    course = await CoursesORM.find_one(id = course_id)
    if not course: raise HTTPException(status_code = 404, detail = 'Curso não encontrado')

    questions = await QuestionsORM.find_many(course_id = course_id)
    if not questions: raise HTTPException(status_code = 404, detail = 'Curso não possui questões')

    await QuestionsORM.delete(course_id = course_id)
    for question in questions:
        await QuestionsAnswersORM.delete(question_id = question.id)
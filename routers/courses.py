from fastapi import HTTPException, status, Header
from routers import router

from typing import List

from models.courses import CourseResponse
from models.classes import ClassCurrent
from models.questions import QuestionAnswersResponse, QuestionResponse, QuestionCorrected, QuestionCorrectedResponse
from database.courses import CoursesORM
from database.classes import ClassesORM
from database.material import MaterialORM
from database.questions import QuestionsORM
from database.questions_answers import QuestionsAnswersORM


@router.get("/courses", status_code = 200, response_model = List[CourseResponse])
async def courses_get():
    courses = await CoursesORM.find_many()
    response = []

    for course in courses:
        class_ = await ClassesORM.find_one(course_id = course.id)
        data = CourseResponse(class_id = class_.id if class_ else None, **course.dict())
        response.append(data)

    return response


@router.get("/courses/{course_id}/class/{class_id}", status_code = 200, response_model = ClassCurrent)
async def classe_get(course_id: int, class_id: int):
    class_ = await ClassesORM.find_one(id = class_id)
    if not class_ or class_.course_id != course_id:
        raise HTTPException(status_code = 404, detail = 'Aulas não encontradas')

    classes = await ClassesORM.find_many(course_id = course_id)
    
    next_classes = [c.dict() for c in classes if isinstance(c.dict(), dict)]
    next_classes = sorted(next_classes, key = lambda c: c.get('order'))
    material = await MaterialORM.find_one(course_id = course_id)
    
    response = ClassCurrent(
        current = class_.dict(), 
        next_classes = next_classes,
        material = material.file if material else None
    )
    
    return response


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


@router.post("/courses/{course_id}/questions", status_code = 201, response_model = QuestionCorrectedResponse)
async def question_corrected(course_id: int, answers: List[QuestionCorrected]):
    course = await CoursesORM.find_one(id = course_id)
    if not course: raise HTTPException(status_code = 404, detail = 'Curso não encontrado')

    questions = await QuestionsORM.find_many(course_id = course_id)
    correct_quantity = 0

    for answer in answers:
        question_answer = await QuestionsAnswersORM.find_one(id = answer.answer_id, question_id = answer.question_id, correct = True)
        correct_quantity += 1 if question_answer else 0

    return QuestionCorrectedResponse(correct_quantity = correct_quantity, total = len(questions))
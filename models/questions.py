from pydantic import BaseModel
from typing import List


class QuestionAnswers(BaseModel):
    option: str
    correct: bool = False


class Question(BaseModel):
    statement: str
    answers: List[QuestionAnswers]


class QuestionAnswersResponse(QuestionAnswers):
    id: int
    question_id: int
    order: int


class QuestionResponse(BaseModel):
    id: int
    course_id: int
    statement: str
    question_answers: List[QuestionAnswersResponse] = []
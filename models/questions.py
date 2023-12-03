from pydantic import BaseModel
from typing import List, Optional


class QuestionAnswers(BaseModel):
    option: str
    correct: bool = False


class Question(BaseModel):
    statement: str
    answers: List[QuestionAnswers]

class QuestionPut(Question):
    id: int


class QuestionAnswersResponse(QuestionAnswers):
    id: int
    question_id: int
    order: int


class QuestionResponse(BaseModel):
    id: int
    course_id: int
    statement: str
    answers: List[QuestionAnswersResponse] = []


class QuestionCorrected(BaseModel):
    question_id: int
    answer_id: int


class QuestionCorrectedResponse(BaseModel):
    correct_quantity: int
    total: int
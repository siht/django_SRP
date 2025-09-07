# polls/question_service.py
from datetime import date
from typing import TypedDict

from django.utils.timezone import now

from .models import Question


class RequiredQuestionData(TypedDict):
    question_text: str


class OptionalQuestionData(TypedDict, total=False):
    pub_date: date


class QuestionData(RequiredQuestionData, OptionalQuestionData):
    pass


def create_question(data: QuestionData) -> Question:
    pub_date = now()
    data.update({'pub_date': pub_date})
    instance = Question(**data)
    instance.save()
    return instance

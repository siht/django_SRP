# polls/question_service.py
from dataclasses import dataclass
from datetime import datetime
from typing import (
    Optional,
    TypedDict,
)

from django.utils.timezone import now

from .models import Question


class RequiredQuestionData(TypedDict):
    question_text: str


class OptionalQuestionData(TypedDict, total=False):
    pub_date: datetime


class QuestionData(RequiredQuestionData, OptionalQuestionData):
    pass


# Implementaciones concretas para CreateQuestion
def get_question_data(self) -> QuestionData:
    question_data: QuestionData = {
        'question_text': self.question_text,
        'pub_date': self.pub_date if self.pub_date else now(),
    }
    return question_data


def django_make_question_object(self, question_data: QuestionData) -> Question:
    question = Question(**question_data)
    return question


def django_save_question_object(self, question: Question) -> Question:
    question.save()
    return question


# Decorador para inyectar métodos en una clase
def inject_methods(**methods):
    def decorator(cls):
        for name, method in methods.items():
            setattr(cls, name, method)
        return cls
    return decorator


# Aplicamos monkey patching a CreateQuestion
@inject_methods(
    get_question_data=get_question_data,
    make_question_object=django_make_question_object,
    save_question_object=django_save_question_object
)
@dataclass
class CreateQuestion:
    question_text: str
    pub_date: Optional[datetime] = None

    def execute(self) -> Question:
        question_data = self.get_question_data()
        question = self.make_question_object(question_data)
        question_saved = self.save_question_object(question)
        return question_saved
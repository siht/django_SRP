# polls/question_service.py
from dataclasses import dataclass
from datetime import datetime
from typing import (
    Any,
    Optional,
    Protocol,
    runtime_checkable,
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


class PullerQuestionDataMixin:
    def get_question_data(self) -> QuestionData:
        question_data: QuestionData = {
            'question_text': self.question_text,
            'pub_date': self.pub_date if self.pub_date else now(),
        }
        return question_data


class DjangoFactoryQuestionMixin:
    def make_question_object(self, question_data: QuestionData) -> Question:
        question = Question(**question_data)
        return question


class DjangoCreateQuestionMixin:
    def save_question_object(self, question: Question) -> Question:
        question.save()
        return question


@dataclass
class CreateQuestion(PullerQuestionDataMixin, DjangoFactoryQuestionMixin, DjangoCreateQuestionMixin):
    question_text: str
    pub_date: Optional[datetime] = None

    def execute(self) -> Question:
        question_data = self.get_question_data()
        question = self.make_question_object(question_data)
        question_saved = self.save_question_object(question)
        return question_saved

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


@runtime_checkable
class IServiceExecutor(Protocol):
    def execute(self) -> Any:
        pass


@runtime_checkable
class IPullerQuestionData(Protocol):
    def get_question_data(self) -> QuestionData:
        pass


@runtime_checkable
class IFactoryQuestion(Protocol):
    def make_question_object(self, question_data: QuestionData) -> Question:
        pass


@runtime_checkable
class ICreateQuestion(Protocol):
    def save_question_object(self, question: Question) -> Question:
        pass


@dataclass
class CreateQuestion:
    question_text: str
    pub_date: Optional[datetime] = None

    def get_question_data(self) -> QuestionData:
        question_data: QuestionData = {
            'question_text': self.question_text,
            'pub_date': self.pub_date if self.pub_date else now(),
        }
        return question_data

    def make_question_object(self, question_data: QuestionData) -> Question:
        question = Question(**question_data)
        return question

    def save_question_object(self, question: Question) -> Question:
        question.save()
        return question

    def execute(self) -> Question:
        question_data = self.get_question_data()
        question = self.make_question_object(question_data)
        question_saved = self.save_question_object(question)
        return question_saved

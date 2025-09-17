# polls/question_service.py
from dataclasses import dataclass
from datetime import datetime
from typing import (
    Optional,
    Protocol,
    TypedDict,
    Any,
    runtime_checkable
)
from django.utils.timezone import now
from .models import Question


class RequiredQuestionData(TypedDict):
    question_text: str


class OptionalQuestionData(TypedDict, total=False):
    pub_date: datetime


class QuestionData(RequiredQuestionData, OptionalQuestionData):
    pass


class IQuestionDataBuilder(Protocol):
    def build(self) -> QuestionData: ...


class IQuestionFactory(Protocol):
    def create(self, question_data: QuestionData) -> Question: ...


class IQuestionRepository(Protocol):
    def save(self, question: Question) -> Question: ...


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
class QuestionDataBuilder:
    question_text: str
    pub_date: Optional[datetime] = None
    
    def build(self) -> QuestionData:
        """
        Construye y retorna el diccionario de datos para crear una pregunta.

            >>> builder = QuestionDataBuilder("¿Doctest funciona?")
            >>> data = builder.build()
            >>> assert 'question_text' in data
            >>> assert data['question_text'], '¿Doctest funciona?'
            >>> assert 'pub_date' in data
        """
        return {
            'question_text': self.question_text,
            'pub_date': self.pub_date if self.pub_date else now(),
        }


@dataclass
class QuestionFactory:
    def create(self, question_data: QuestionData) -> Question:
        """
        Crea una instancia de Question a partir de datos primitivos.

            >>> factory = QuestionFactory()
            >>> data = {'question_text': 'Test?', 'pub_date': now()}
            >>> question = factory.create(data)
            >>> isinstance(question, Question)
            True
            >>> question.question_text
            'Test?'
        """
        return Question(**question_data)


@dataclass  
class QuestionRepository:
    def save(self, question: Question) -> Question:
        """
        Persiste la pregunta en la base de datos. 
        
            >>> repo = QuestionRepository()
            >>> new_question = Question(question_text="Test Save", pub_date=now())
            >>> saved_question = repo.save(new_question)
            >>> assert saved_question.id is not None
        """
        question.save()
        return question


@dataclass
class CreateQuestion:
    data_builder: IQuestionDataBuilder
    question_factory: IQuestionFactory
    question_repository: IQuestionRepository
    
    def execute(self) -> Question:
        question_data = self.data_builder.build()
        question = self.question_factory.create(question_data)
        return self.question_repository.save(question)


def create_question_service(question_text: str, pub_date: Optional[datetime] = None) -> CreateQuestion:
    data_builder = QuestionDataBuilder(question_text=question_text, pub_date=pub_date)
    question_factory = QuestionFactory()
    question_repository = QuestionRepository()
    
    return CreateQuestion(
        data_builder=data_builder,
        question_factory=question_factory,
        question_repository=question_repository
    )

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


class RepositoryError(Exception):
    """Excepción base para todos los errores relacionados con el repositorio."""
    pass


class QuestionNotFound(RepositoryError):
    """
    Se lanza cuando un Question con el ID especificado no puede ser encontrado.
    """
    def __init__(self, message: str):
        super().__init__(message)


class RequiredQuestionData(TypedDict):
    question_text: str


class OptionalQuestionData(TypedDict, total=False):
    pub_date: datetime


class QuestionData(RequiredQuestionData, OptionalQuestionData):
    pass


@dataclass
class QuestionDTO:
    """Entidad de dominio - solo datos, sin lógica"""
    id: int
    question_text: str
    pub_date: datetime


@dataclass
class QuestionCreateDTO:
    """Entidad de dominio - solo datos, sin lógica"""
    question_text: str
    pub_date: Optional[datetime] = None


class IQuestionRepository(Protocol):
    def create(self, question: QuestionCreateDTO) -> QuestionDTO: ...
    def get_by_id(self, question_id: int) -> QuestionDTO | None | QuestionNotFound: ...
    def get_recent(self, limit: int=5) -> list[QuestionDTO]: ...


@runtime_checkable
class IServiceExecutor(Protocol):
    def execute(self) -> Any:
        pass


@dataclass  
class QuestionRepository:
    def create(self, question: QuestionCreateDTO) -> QuestionDTO:
        """
        Persiste la pregunta en la base de datos. 
        
            >>> repo = QuestionRepository()
            >>> dto = QuestionCreateDTO(question_text="Test Save", pub_date=now())
            >>> created_question = repo.create(dto)
            >>> assert created_question.id is not None
            >>> assert isinstance(created_question, QuestionDTO)
        """
        create_question_args = {
            'question_text': question.question_text,
            'pub_date': question.pub_date if question.pub_date else now()
        }
        django_question = Question.objects.create(**create_question_args)
        question_dto = (
            QuestionDTO(
                id=django_question.id,
                question_text=question.question_text,
                pub_date=django_question.pub_date
            )
        )
        return question_dto

    def get_by_id(self, question_id: int) -> QuestionDTO | None | QuestionNotFound:
        try:
            django_question = (
                Question.objects
                .values('id', 'question_text', 'pub_date')
                .get(id=question_id)
            )
        except Question.DoesNotExist as err:
            raise QuestionNotFound(f"El 'Question' con ID {question_id} no existe.")
        return QuestionDTO(**django_question)

    def get_recent(self, limit: int=5) -> list[QuestionDTO]:
        django_recent_questions = (
            Question.objects
            .values('id', 'question_text', 'pub_date')
            .order_by('-pub_date')[:limit]
        )
        return [QuestionDTO(**choice) for choice in django_recent_questions]


@dataclass
class CreateQuestion:
    question_repository: IQuestionRepository
    question: QuestionCreateDTO
    
    def execute(self) -> QuestionDTO:
        return self.question_repository.create(self.question)


def create_question_service(question: QuestionCreateDTO) -> CreateQuestion:
    question_repository = QuestionRepository()
    
    return CreateQuestion(
        question_repository=question_repository,
        question=question
    )

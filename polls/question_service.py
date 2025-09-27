# polls/question_service.py
from dataclasses import dataclass
from django.utils.timezone import now
from zope.interface import implementer

from business_logic.dtos import QuestionDTO
from business_logic.exceptions import QuestionNotFound
from business_logic.interfaces import IQuestionRepository
from business_logic.use_cases import CreateQuestion

from .models import Question


@implementer(IQuestionRepository)
class DjangoQuestionRepository:
    def __init__(self, service):
        self.service = service

    def create(self, question: QuestionDTO) -> QuestionDTO:
        """
        Persiste la pregunta en la base de datos. 
        
            >>> repo = DjangoQuestionRepository()
            >>> dto = QuestionDTO(question_text="Test Save", pub_date=now())
            >>> created_question = repo.create(dto)
            >>> assert created_question.id is not None
            >>> assert isinstance(created_question, QuestionDTO)
        """
        es_para_nueva_creacion_y_no_tiene_fecha = (
            not question.id and not question.pub_date
        )
        if es_para_nueva_creacion_y_no_tiene_fecha:
            question.pub_date = now()
        create_question_args = {
            'question_text': question.question_text,
            'pub_date': question.pub_date
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


def create_question_service(question: QuestionDTO) -> CreateQuestion:
    question_repository = DjangoQuestionRepository()
    
    return CreateQuestion(
        question_repository=question_repository,
        question=question
    )

# business_logic/use_cases.py

# como ven nos faltan los test de integración para esta logica de negocio
from dataclasses import dataclass
from zope.interface import implementer

from .dtos import (
    ChoiceDTO,
    QuestionDTO,
)
from .exceptions import ChoiceNotFound
from .interfaces import (
    IChoiceRepository,
    ICreateChoiceExecutor,
    ICreateQuestionExecutor,
    IQuestionRepository,
    IVoteExecutor,
)


@implementer(ICreateQuestionExecutor)
class CreateQuestion:
    def __init__(self, service):
        self.service = service
        self.question_repository = IQuestionRepository(self.service)

    def execute(self, question: QuestionDTO) -> QuestionDTO:
        return self.question_repository.create(question)


@implementer(ICreateChoiceExecutor)
class CreateChoice:
    def __init__(self, service):
        self.service = service
        self.choice_repository = IChoiceRepository(self.service)

    def execute(self, choice_data: ChoiceDTO) -> ChoiceDTO:
        return self.choice_repository.create(choice_data)


@implementer(IVoteExecutor)
class Vote:
    def __init__(self, service):
        self.service = service
        self.choice_repository = IChoiceRepository(self.service)

    def execute(self, choice_id: int) -> ChoiceDTO | None | ChoiceNotFound:
        choice = self.choice_repository.get_by_id(choice_id)
        self.choice_repository.update_votes(choice_id)
        return choice

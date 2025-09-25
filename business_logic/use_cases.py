# business_logic/use_cases.py

# como ven nos faltan los test de integración para esta logica de negocio
from dataclasses import dataclass

from .dtos import (
    ChoiceDTO,
    QuestionDTO,
)
from .exceptions import ChoiceNotFound
from .interfaces import (
    IChoiceRepository,
    IQuestionRepository,
    IServiceExecutor, # esta se usa aunque no se vea
)


@dataclass
class CreateQuestion:
    question_repository: IQuestionRepository
    question: QuestionDTO
    
    def execute(self) -> QuestionDTO:
        return self.question_repository.create(self.question)


@dataclass
class CreateChoice:
    choice_repository: IChoiceRepository
    choice_data: ChoiceDTO

    def execute(self) -> ChoiceDTO:
        return self.choice_repository.create(self.choice_data)


@dataclass
class Vote:
    choice_repository: IChoiceRepository
    choice_id: int

    def execute(self) -> ChoiceDTO | None | ChoiceNotFound:
        choice = self.choice_repository.get_by_id(self.choice_id)
        self.choice_repository.update_votes(self.choice_id)
        return choice

# business_logic/interfaces.py

from zope.interface import Interface

from . exceptions import (
    ChoiceNotFound,
    QuestionNotFound,
)
from .dtos import (
    ChoiceDTO,
    QuestionDTO,
)


class IQuestionRepository(Interface):
    def create(question: QuestionDTO) -> QuestionDTO:
        """Return a QuestionDTO"""

    def get_by_id(question_id: int) -> QuestionDTO | None | QuestionNotFound:
        """Return a QuestionDTO if a question was found else raise QuestionNotFound"""

    def get_recent(limit: int=5) -> list[QuestionDTO]:
        """Return a list[QuestionDTO] limited by limit"""


class IChoiceRepository(Interface):
    """
    Define las operaciones mínimas para un repositorio que maneja 'Choice'.
    """
    
    def get_by_id(choice_id: int) -> ChoiceDTO | None | ChoiceNotFound:
        """Return a ChoiceDTO if a choice was found else raise ChoiceNotFound."""
        
    def get_all() -> list[ChoiceDTO]:
        """Return a list[ChoiceDTO] of all choices."""

    def update_votes(choice_id: int) -> int:
        """Return int the actual votes and update vote counter for an specific Choice."""

    def create(choice: ChoiceDTO) -> ChoiceDTO:
        """Return a ChoiceDTO. create a new Choice"""

    def update(choice: ChoiceDTO) -> ChoiceDTO | None:
        """Return ChoiceDTO. updates with the info of the ChoiceDTO."""

    def delete(choice_id: int) -> None:
        """Return None, deletes a Choice by int id"""


class ICreateQuestionExecutor(Interface):
    def execute(question: QuestionDTO) -> QuestionDTO:
        """Return a QuestionDTO"""


class ICreateChoiceExecutor(Interface):
    def execute(choice_data: ChoiceDTO) -> ChoiceDTO:
        """Return a ChoiceDTO. create a new Choice"""


class IVoteExecutor(Interface):
    def execute(choice_id: int) -> int:
        """Return int the actual votes and update vote counter for an specific Choice."""

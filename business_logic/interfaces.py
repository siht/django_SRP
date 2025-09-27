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
    def create(self, question: QuestionDTO) -> QuestionDTO:
        """Return a QuestionDTO"""

    def get_by_id(self, question_id: int) -> QuestionDTO | None | QuestionNotFound:
        """Return a QuestionDTO if a question was found else raise QuestionNotFound"""

    def get_recent(self, limit: int=5) -> list[QuestionDTO]:
        """Return a list[QuestionDTO] limited by limit"""


class IChoiceRepository(Interface):
    """
    Define las operaciones mínimas para un repositorio que maneja 'Choice'.
    """
    
    def get_by_id(self, choice_id: int) -> ChoiceDTO | None | ChoiceNotFound:
        """Return a ChoiceDTO if a choice was found else raise ChoiceNotFound."""
        
    def get_all(self) -> list[ChoiceDTO]:
        """Return a list[ChoiceDTO] of all choices."""

    def update_votes(self, choice_id: int) -> int:
        """Return int the actual votes and update vote counter for an specific Choice."""

    def create(self, choice: ChoiceDTO) -> ChoiceDTO:
        """Return a ChoiceDTO. create a new Choice"""

    def update(self, choice: ChoiceDTO) -> ChoiceDTO | None:
        """Return ChoiceDTO. updates with the info of the ChoiceDTO."""

    def delete(self, choice_id: int) -> None:
        """Return None, deletes a Choice by int id"""


class ICreateQuestionExecutor(Interface):
    def execute(self, question: QuestionDTO) -> QuestionDTO:
        """Return a QuestionDTO"""


class ICreateChoiceExecutor(Interface):
    def execute(self, choice_data: ChoiceDTO) -> ChoiceDTO:
        """Return a ChoiceDTO. create a new Choice"""
        pass


class IVoteExecutor(Interface):
    def execute(self, choice_id: int) -> int:
        """Return int the actual votes and update vote counter for an specific Choice."""

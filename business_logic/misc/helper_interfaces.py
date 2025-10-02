# business_logic/misc/helper_interfaces.py

from typing import Any
from zope.interface import Interface

from business_logic.dtos import (
    ChoiceDTO,
    QuestionDTO,
)


class IVoteIOFrameworkAdapter(Interface):
    def input(input: Any) -> int:
        """Return integer. Is the choice id"""

    def output(choice: ChoiceDTO) -> Any:
        """Return something related with Choice. """

    def execute(input: Any) -> Any:
        """Return something related with Choice"""


class IQuestionCreatorIOFrameworkAdapter(Interface):
    def input(input: Any) -> QuestionDTO:
        """Return QuestionDTO"""

    def output(question: QuestionDTO) -> Any:
        """Return something related with Question"""

    def execute(input: Any) -> Any:
        """Return something related with Question"""


class IChoiceCreatorIOFrameworkAdapter(Interface):
    def input(input: Any) -> ChoiceDTO:
        """Return ChoiceDTO"""

    def output(choice: ChoiceDTO) -> Any:
        """Return something related with Choice"""

    def execute(input: Any) -> Any:
        """Return something related with Choice"""

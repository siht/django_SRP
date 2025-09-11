# polls/choice_service.py
from dataclasses import dataclass
from typing import (
    Any,
    Protocol,
    TypedDict,
)

from django.db.models import F

from .models import Choice


class ChoiceData(TypedDict):
    choice_text: str
    question_id: int


class VoteData(TypedDict):
    choice_text: Choice


class IServiceExecutor(Protocol):
    def execute(self) -> Any:
        pass


class ChoicePullerData(Protocol):
    def get_choice_data(self) -> ChoiceData:
        pass


class ChoiceFactory(Protocol):
    def build_choice(self, data: ChoiceData) -> Choice:
        pass


class PersistChoice(Protocol):
    def save_choice(saelf, choice: Choice) -> Choice:
        pass


class ChoiceGetter(Protocol):
    def get_choice_from_data(self) -> Choice:
        pass


class UpdateCounterVotesChoice(Protocol):
    def update_choice_counter(self, choice) -> Choice:
        pass


@dataclass
class CreateChoice:
    choice_text: str
    question_id: int

    def get_choice_data(self) -> ChoiceData:
        return {'choice_text': self.choice_text, 'question_id': self.question_id}

    def build_choice(self, data: ChoiceData) -> Choice:
        choice = Choice(**data)
        return choice

    def save_choice(self, choice: Choice) -> Choice:
        choice.save()
        return choice

    def execute(self) -> Choice:
        data = self.get_choice_data()
        choice = self.build_choice(data)
        saved_choice = self.save_choice(choice)
        return saved_choice


@dataclass
class Vote:
    data: VoteData

    def get_choice_from_data(self) -> Choice:
        return self.data['choice_text']

    def update_choice_counter(self, choice) -> Choice:
        choice.votes = F('votes') + 1
        return choice
    
    def save_choice(saelf, choice: Choice) -> Choice:
        choice.save()
        return choice

    def execute(self) -> Choice:
        choice = self.get_choice_from_data()
        choice_changed = self.update_choice_counter(choice)
        choice_updated = self.save_choice(choice_changed)
        return choice_updated

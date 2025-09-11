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

# Implementaciones concretas para CreateChoice
def choice_get_choice_data(self) -> ChoiceData:
    return {'choice_text': self.choice_text, 'question_id': self.question_id}

def django_build_choice(self, data: ChoiceData) -> Choice:
    choice = Choice(**data)
    return choice

def django_save_choice(self, choice: Choice) -> Choice:
    choice.save()
    return choice

# Implementaciones concretas para Vote
def django_get_choice_from_data(self) -> Choice:
    return self.data['choice_text']

def django_update_choice_counter(self, choice) -> Choice:
    choice.votes = F('votes') + 1
    return choice

def django_save_choice_vote(self, choice: Choice) -> Choice:
    choice.save()
    return choice

# Decorador para inyectar métodos en una clase
def inject_methods(**methods):
    def decorator(cls):
        for name, method in methods.items():
            setattr(cls, name, method)
        return cls
    return decorator


@inject_methods(
    get_choice_data=choice_get_choice_data,
    build_choice=django_build_choice,
    save_choice=django_save_choice
)
@dataclass
class CreateChoice:
    choice_text: str
    question_id: int

    def execute(self) -> Choice:
        data = self.get_choice_data()
        choice = self.build_choice(data)
        saved_choice = self.save_choice(choice)
        return saved_choice


@inject_methods(
    get_choice_from_data=django_get_choice_from_data,
    update_choice_counter=django_update_choice_counter,
    save_choice=django_save_choice_vote
)
@dataclass
class Vote:
    data: VoteData

    def execute(self) -> Choice:
        choice = self.get_choice_from_data()
        choice_changed = self.update_choice_counter(choice)
        choice_updated = self.save_choice(choice_changed)
        return choice_updated

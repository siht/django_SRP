# polls/choice_service.py
from typing import TypedDict

from django.db.models import F

from .models import Choice


class ChoiceData(TypedDict):
    choice_text: str
    question_id: int


class VoteData(TypedDict):
    choice_text: Choice


def create_choice(data: ChoiceData) -> Choice:
    return Choice.objects.create(**data)


def vote(data: VoteData) -> Choice:
    choice = data['choice_text']
    choice.votes = F('votes') + 1
    choice.save()
    return choice

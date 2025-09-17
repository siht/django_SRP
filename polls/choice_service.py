# polls/choice_service.py
from dataclasses import dataclass
from typing import (
    Any,
    Protocol,
    TypedDict,
    runtime_checkable,
)

from django.db.models import F
from .models import Choice, Question


class ChoiceData(TypedDict):
    choice_text: str
    question_id: int


class VoteData(TypedDict):
    choice_text: Choice


@runtime_checkable
class IServiceExecutor(Protocol):
    def execute(self) -> Any:
        pass


class IChoiceDataBuilder(Protocol):
    def build(self) -> ChoiceData:
        pass


class IChoiceFactory(Protocol):
    def create(self, choice_data: ChoiceData) -> Choice:
        pass


class IChoiceRepository(Protocol):
    def save(self, choice: Choice) -> Choice:
        pass


class IChoiceGetter(Protocol):
    def get(self) -> Choice:
        pass


class IVoteUpdater(Protocol):
    def update(self, choice: Choice) -> Choice:
        pass


@dataclass
class ChoiceDataBuilder:
    choice_text: str
    question_id: int

    def build(self) -> ChoiceData:
        """
        Construye y retorna el diccionario de datos para crear una opción.
        
        >>> builder = ChoiceDataBuilder("Test Choice", 1)
        >>> data = builder.build()
        >>> assert 'choice_text' in data
        >>> assert data['choice_text'] == 'Test Choice'
        >>> assert 'question_id' in data
        >>> assert data['question_id'] == 1
        """
        return {
            'choice_text': self.choice_text,
            'question_id': self.question_id,
        }


@dataclass
class DjangoChoiceFactory:
    def create(self, choice_data: ChoiceData) -> Choice:
        """
        Crea una instancia de Choice a partir de datos primitivos.
        
        >>> from django.utils.timezone import now
        >>> question = Question("se va a hacer o no se va a hacer", pub_date=now())
        >>> data = {'choice_text': 'A choice', 'question_id': question.id}
        >>> factory = DjangoChoiceFactory()
        >>> choice = factory.create(data)
        >>> assert choice.choice_text == 'A choice'
        """
        return Choice(**choice_data)


@dataclass
class DjangoChoiceRepository:
    def save(self, choice: Choice) -> Choice:
        """
        Persiste una opción en la base de datos.
        
        >>> from django.utils.timezone import now
        >>> question = Question(question_text="se va a hacer o no se va a hacer", pub_date=now())
        >>> question.save()
        >>> choice = Choice(question=question, choice_text='no')
        >>> repo = DjangoChoiceRepository()
        >>> saved_choice = repo.save(choice)
        >>> assert saved_choice.id is not None
        """
        choice.save()
        return choice


@dataclass
class DjangoChoiceGetter:
    data: VoteData

    def get(self) -> Choice:
        """
        Obtiene el objeto Choice del diccionario de datos.
        
        >>> from django.utils.timezone import now
        >>> question = Question(question_text="se va a hacer o no se va a hacer", pub_date=now())
        >>> question.save()
        >>> choice = Choice(question=question, choice_text='no')
        >>> getter = DjangoChoiceGetter({'choice_text': choice})
        >>> choice = getter.get()
        >>> assert isinstance(choice, Choice)
        """
        return self.data['choice_text']


@dataclass
class DjangoVoteCounterUpdater:
    def update(self, choice: Choice) -> Choice:
        """
        Incrementa el contador de votos de una opción.
        
        >>> from django.utils.timezone import now
        >>> from django.db.models import Value
        >>> from django.db.models.expressions import CombinedExpression
        >>> question = Question(question_text="se va a hacer o no se va a hacer", pub_date=now())
        >>> question.save()
        >>> choice = Choice(question=question, choice_text='no')
        >>> choice.save()
        >>> updater = DjangoVoteCounterUpdater()
        >>> updated_choice = updater.update(choice)
        >>> assert isinstance(choice.votes, CombinedExpression)
        >>> assert isinstance(choice.votes.lhs, F)
        >>> assert choice.votes.lhs.name == 'votes'
        >>> assert choice.votes.connector == '+'
        >>> assert isinstance(choice.votes.rhs, Value)
        >>> assert choice.votes.rhs.value == 1
        """
        choice.votes = F('votes') + 1
        return choice


# Casos de uso
@dataclass
class CreateChoice:
    data_builder: IChoiceDataBuilder
    choice_factory: IChoiceFactory
    choice_repository: IChoiceRepository

    def execute(self) -> Choice:
        data = self.data_builder.build()
        choice = self.choice_factory.create(data)
        return self.choice_repository.save(choice)


@dataclass
class Vote:
    choice_getter: IChoiceGetter
    counter_updater: IVoteUpdater
    choice_repository: IChoiceRepository

    def execute(self) -> Choice:
        choice = self.choice_getter.get()
        updated_choice = self.counter_updater.update(choice)
        return self.choice_repository.save(updated_choice)


def create_choice_service(choice_text: str, question_id: int) -> CreateChoice:
    data_builder = ChoiceDataBuilder(choice_text=choice_text, question_id=question_id)
    choice_factory = DjangoChoiceFactory()
    choice_repository = DjangoChoiceRepository()

    return CreateChoice(
        data_builder=data_builder,
        choice_factory=choice_factory,
        choice_repository=choice_repository,
    )


def vote_service(cleaned_data: dict) -> Vote:
    choice_getter = DjangoChoiceGetter(data=cleaned_data)
    counter_updater = DjangoVoteCounterUpdater()
    choice_repository = DjangoChoiceRepository()

    return Vote(
        choice_getter=choice_getter,
        counter_updater=counter_updater,
        choice_repository=choice_repository,
    )

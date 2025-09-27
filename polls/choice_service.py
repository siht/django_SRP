# polls/choice_service.py
from typing import Any
from zope.interface import implementer

from django.db.models import F

from business_logic.dtos import ChoiceDTO
from business_logic.exceptions import ChoiceNotFound, ChoiceDataError
from business_logic.interfaces import IChoiceRepository

from .models import Choice


@implementer(IChoiceRepository)
class DjangoChoiceRepository:
    def __init__(self, service):
        self.service = service

    def get_by_id(self, choice_id: int) -> ChoiceDTO | None | ChoiceNotFound:
        """Obtiene un DTO de un Choice por su ID.
            
            >>> from polls.models import Choice, Question
            >>> from django.utils.timezone import now

            # Creamos un objeto de prueba en la base de datos
            >>> question = Question.objects.create(question_text="¿Cuál es tu color favorito?", pub_date=now())
            >>> choice_instance = Choice.objects.create(question=question, choice_text="azul", votes=10)
            
            # Instanciamos el repositorio
            >>> repo = DjangoChoiceRepository()
            
            # Caso 1: El objeto existe, retorna un DTO
            >>> result = repo.get_by_id(choice_instance.id)
            >>> assert isinstance(result, ChoiceDTO)
            >>> assert result.text == 'azul'
            >>> assert result.votes == 10
            
            # Caso 2: El objeto no existe, retorna None
            >>> result = repo.get_by_id(999) # un ID que no existe
            >>> assert result is None
        """
        try:
            # Traer los datos directamente como un diccionario
            choice = (
                Choice.objects.filter(id=choice_id)
                .annotate(text=F('choice_text'))
                .values('id', 'text', 'votes', 'question_id').first()
            )
            if choice:
                return ChoiceDTO(**choice)
            return None
        except Choice.DoesNotExist:
            raise ChoiceNotFound(f"El 'Choice' con ID {choice_id} no existe.")

    def get_all(self) -> list[ChoiceDTO]:
        """Obtiene una lista de todos los DTOs de Choice.
        
        >>> from polls.models import Choice, Question
        >>> from django.utils.timezone import now
        
        # Creamos objetos de prueba en la base de datos
        >>> _ = Choice.objects.all().delete() # para limpiar la db por si las dudas
        >>> question1 = Question.objects.create(question_text="Pregunta 1", pub_date=now())
        >>> choice1 = Choice.objects.create(question=question1, choice_text="Opción 1", votes=5)
        >>> choice2 = Choice.objects.create(question=question1, choice_text="Opción 2", votes=10)
        
        # Instanciamos el repositorio
        >>> repo = DjangoChoiceRepository()
        
        # Obtenemos todos los DTOs
        >>> all_choices = repo.get_all()
        >>> assert len(all_choices) >= 2
        >>> first_dto = all_choices[0]
        >>> assert isinstance(first_dto, ChoiceDTO)
        >>> assert first_dto.text == 'Opción 1'
        >>> assert first_dto.votes == 5
        """
        # Se obtienen todos los objetos Choice y se transforman en una lista de DTOs
        choices = (
            Choice.objects.all()
            .annotate(text=F('choice_text'))
            .values('id', 'text', 'votes', 'question_id')
        )
        return [ChoiceDTO(**choice) for choice in choices]

    def update_votes(self, choice_id: int) -> int:
        """
        Incrementa el contador de votos de una opción.
        
            >>> from django.utils.timezone import now
            >>> from django.db.models import Value
            >>> from django.db.models.expressions import CombinedExpression
            >>> from .models import Question
            >>> question = Question(question_text="se va a hacer o no se va a hacer", pub_date=now())
            >>> question.save()
            >>> choice = Choice(question=question, choice_text='no')
            >>> choice.save()
            >>> votes = choice.votes
            >>> repo = DjangoChoiceRepository()
            >>> id_choice = choice.id
            >>> updated_choice = repo.update_votes(id_choice)
            >>> choice.refresh_from_db()
            >>> assert choice.votes == votes + 1
        """
        # Lógica para actualizar los votos directamente en la base de datos
        rows_affected = Choice.objects.filter(id=choice_id).update(votes=F('votes') + 1)
        return rows_affected

    def create(self, choice: ChoiceDTO) -> ChoiceDTO:
        """
        Persiste una opción en la base de datos.
        
            >>> from django.utils.timezone import now
            >>> from .models import Question
            >>> question = Question(question_text="se va a hacer o no se va a hacer", pub_date=now())
            >>> question.save()
            >>> choice = ChoiceDTO(question_id=question.id, text='no')
            >>> repo = DjangoChoiceRepository()
            >>> saved_choice = repo.create(choice)
            >>> assert saved_choice.id is not None
        """
        if not choice.question_id:
            raise ChoiceDataError() # esto no debería pasar por la validación del DTO, pero mypy no perdona
        new_choice = Choice.objects.create(
            question_id=choice.question_id,
            choice_text=choice.text,
            votes=choice.votes or 0
        )
        # Aquí creas y retornas la instancia del DTO con el ID generado por la base de datos
        choice.id = new_choice.id
        return choice

    def update(self, choice: ChoiceDTO) -> ChoiceDTO | None:
        """
        Actualiza una opción en la base de datos.

            >>> from django.utils.timezone import now
            >>> from .models import Question
            >>> question = Question(question_text="se va a hacer o no se va a hacer", pub_date=now())
            >>> question.save()
            >>> choice = Choice(question=question, choice_text='no')
            >>> choice.save()
            >>> repo = DjangoChoiceRepository()
            >>> dto_choice = ChoiceDTO(id=choice.id, text='sí, lo vamos a hacer')
            >>> updated_choice = repo.update(dto_choice)
            >>> assert updated_choice.id is not None
        """
        if choice.id is None:
            return None
        data_not_null_for_update: dict[str, Any] = {}
        if choice.text is not None:
            data_not_null_for_update.update(choice_text=choice.text)
        if choice.votes is not None:
            data_not_null_for_update.update(votes=choice.votes)
        rows_affected = Choice.objects.filter(id=choice.id).update(
            **data_not_null_for_update
        )
        if rows_affected > 0:
            # Aquí creas y retornas la instancia del DTO con la información actualizada.
            django_choice = Choice.objects.get(id=choice.id)
            return ChoiceDTO(
                id=choice.id,
                question_id=django_choice.id,
                text=django_choice.choice_text,
                votes=django_choice.votes
            )
        else:
            # Manejar el caso de que el objeto no exista
            raise Choice.DoesNotExist

    def delete(self, choice_id: int) -> None:
        """
        Elimina el Choice por su ID.

            >>> from polls.models import Question
            >>> from django.utils.timezone import now
            
            >>> question = Question.objects.create(question_text="¿Cuál es tu color favorito?", pub_date=now())
            >>> choice_instance = Choice.objects.create(question=question, choice_text="azul", votes=10)
            
            >>> assert Choice.objects.filter(id=choice_instance.id).exists()

            >>> repo = DjangoChoiceRepository()
            >>> repo.delete(choice_instance.id)

            >>> assert not Choice.objects.filter(id=choice_instance.id).exists()
        """
        Choice.objects.filter(id=choice_id).delete()

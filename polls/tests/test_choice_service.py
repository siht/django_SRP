# polls/tests/test_choice_service.py
from django.test import TestCase
from django.utils.timezone import now
from polls.models import (
    Choice,
    Question,
)
from polls.choice_service import (
    ChoiceCreateDTO,
    ChoiceDTO,
    create_choice_service,
    vote_service,
)


class CreateChoiceTest(TestCase):
    def test_create_choice(self):
        """
        Prueba que la función create_choice crea una opción correctamente.
        """
        # Crear una pregunta de prueba
        question = Question.objects.create(question_text='¿Cuál es tu color favorito?', pub_date=now())

        # Datos de entrada
        choice_data = ChoiceCreateDTO(question_id=question.id, text='Rojo', votes=None)

        # Llamar a la función
        _choice_service = create_choice_service(choice_data)
        choice = _choice_service.execute()

        # Verificar que la opción se creó correctamente
        self.assertIsInstance(choice, ChoiceDTO)
        self.assertIsNotNone(choice.id)
        self.assertEqual(choice.text, 'Rojo')
        self.assertEqual(choice.question_id, question.id)


class VoteTest(TestCase):
    def test_vote_multiple_times(self):
        """
        Prueba que la función vote incrementa el contador de votos correctamente después de múltiples votos.
        """
        # Crear una pregunta y una opción de prueba, ojo elegir si usar la logica de negocio si es necesario
        # a veces las reglas de negocio encapsulan muchas operaciones, esto es dejado a criterio
        # o si tiene un escenario usar los fixtures para cargar esa data
        question = Question.objects.create(question_text='¿Cuál es tu color favorito?', pub_date=now())
        choice = Choice.objects.create(choice_text='Rojo', question=question, votes=0)
        # Llamar a la función varias veces
        for _ in range(3):
            _vote_service = vote_service(choice_id=choice.id)
            _vote_service.execute()
        # Verificar que el contador de votos se incrementó correctamente
        choice.refresh_from_db()
        self.assertEqual(choice.votes, 3)

# polls/tests/tests_question_service.py
from datetime import timezone as datetime_timezone
from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone

from polls.models import Question
from polls.question_service import (
    create_question,
    QuestionData
)


class CreateQuestionTest(TestCase):
    @patch('polls.question_service.now')
    def test_create_question(self, mock_now): # esta prueba si se podría considerar unitaria
        """
        Prueba que la función create_question crea y guarda una instancia de Question correctamente.
        """
        mocked_now_value = timezone.datetime(2023, 10, 1, 12, 0, 0, tzinfo=datetime_timezone.utc)
        mock_now.return_value = mocked_now_value
        # Datos de entrada
        data: QuestionData = {
            'question_text': '¿Cuál es tu color favorito?'
        }

        # Llamar a la función
        question = create_question(data)
        # Verificar que la pregunta se creó correctamente
        self.assertIsInstance(question, Question)
        self.assertEqual(question.question_text, '¿Cuál es tu color favorito?')
        self.assertIsNotNone(question.pub_date)
        self.assertTrue(question.id)  # Verificar que se guardó en la base de datos
        self.assertEqual(question.pub_date, mocked_now_value)

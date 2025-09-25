# polls/tests/test_forms.py
from unittest.mock import patch

from django.test import TestCase

from polls.forms import FormQuestion

class FormQuestionTest(TestCase):
    def test_valid_data(self):
        """
        Prueba que el formulario acepta datos válidos.
        """
        form_data = {
            'question_text': '¿Cuál es tu color favorito?'
        }
        form = FormQuestion(data=form_data)
        self.assertTrue(form.is_valid())

    def test_question_text_too_long(self):
        """
        Prueba que el formulario rechaza un texto de pregunta demasiado largo.
        """
        form_data = {
            'question_text': 'a' * 201  # Más de 200 caracteres
        }
        form = FormQuestion(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('question_text', form.errors)  # Verifica que hay un error en 'question_text'

    @patch('polls.forms.create_question_service')
    def test_save(self, mock_create_question):
        """
        Prueba que el formulario guarda los datos correctamente.
        """
        form_data = {
            'question_text': '¿Cuál es tu color favorito?'
        }
        form = FormQuestion(data=form_data)
        self.assertTrue(form.is_valid())
        # Llamar a save()
        form.save()
        # Verificar que CreateQuestion fue llamado con los datos correctos
        mock_create_question.assert_called_once()
        call_args = mock_create_question.call_args[0]  # args posicionales
        called_dto = call_args[0] if call_args else mock_create_question.call_args[1]['question']
        self.assertEqual(called_dto.question_text, '¿Cuál es tu color favorito?')
        self.assertIsNone(called_dto.id)
        # No verificamos la fecha exacta, solo que esté presente
        self.assertIsNotNone(called_dto.pub_date)

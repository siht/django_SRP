# polls/tests/test_forms.py
from unittest.mock import patch

from django.test import TestCase

from business_logic.dtos import QuestionDTO
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

    @patch('polls.forms.CreateQuestion.execute')
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
        mock_create_question.assert_called_once_with(
            QuestionDTO(question_text='¿Cuál es tu color favorito?')
        )


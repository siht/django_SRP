# polls/tests/test_serializers.py
from unittest.mock import MagicMock
from unittest.mock import patch

from django.test import TestCase
from django.utils.timezone import now

from business_logic.dtos import ChoiceDTO
from polls.models import (
    Choice,
    Question,
)
from polls.serializers import ChoiceSerializer


class ChoiceSerializerTest(TestCase):
    def test_serialization(self):
        """
        Prueba que el serializer convierte un objeto Choice en un diccionario.
        """
        # Crear una pregunta y una opción de prueba
        question = Question.objects.create(question_text='¿Cuál es tu color favorito?', pub_date=now())
        choice = Choice.objects.create(choice_text='Rojo', question=question)
        # Serializar la opción
        serializer = ChoiceSerializer(choice)
        # Verificar que los datos serializados son correctos
        expected_data = {'choice_text': 'Rojo'}
        self.assertEqual(serializer.data, expected_data)

    def test_deserialization_valid_data(self):
        """
        Prueba que el serializer convierte un diccionario válido en un objeto Choice.
        """
        # Datos de entrada válidos
        data = {'choice_text': 'Rojo'}
        # Deserializar los datos
        serializer = ChoiceSerializer(data=data)
        # Verificar que los datos son válidos
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, data)

    def test_deserialization_invalid_data(self):
        """
        Prueba que el serializer rechaza datos inválidos.
        """
        # Datos de entrada inválidos (choice_text vacío)
        data = {'choice_text': ''}
        # Deserializar los datos
        serializer = ChoiceSerializer(data=data)
        # Verificar que los datos no son válidos
        self.assertFalse(serializer.is_valid())
        self.assertIn('choice_text', serializer.errors)

    @patch('polls.serializers.CreateChoice.execute')
    def test_create(self, mock_create_choice):
        """
        Prueba que el método create llama a create_choice con los datos correctos.
        """
        # Crear una pregunta de prueba
        question = Question.objects.create(question_text='¿Cuál es tu color favorito?', pub_date=now())
        # Datos de entrada
        data = {'choice_text': 'Rojo'}
        # Crear un contexto con el request y el question_id
        context = {
            'request': MagicMock(parser_context={'kwargs': {'pk': question.id}})
        }
        # Deserializar los datos
        serializer = ChoiceSerializer(data=data, context=context)
        # Verificar que los datos son válidos
        self.assertTrue(serializer.is_valid())
        # Llamar al método create
        serializer.create(serializer.validated_data)
        # Verificar que create_choice fue llamado con los datos correctos
        expected_data = ChoiceDTO(question_id=question.id, text='Rojo')
        mock_create_choice.assert_called_once_with(expected_data)

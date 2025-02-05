# polls/tests/tests_integration.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from polls.models import Question


class QuestionTests(TestCase):
    def test_crear_pregunta(self):
        url_page = reverse('polls:index')
        form_data = {'question_text': 'se va a hacer o no se va a hacer?'}
        response = self.client.post(url_page, form_data)
        self.assertEqual(response.status_code, 302)
    
    def test_crear_pregunta_muy_larga(self):
        url_page = reverse('polls:index')
        form_data = {'question_text': 'a'*201}
        response = self.client.post(url_page, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('errorlist', response.content.decode('utf-8'))


class VotoTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.question = (
            Question.objects
            .create(
                question_text='pregunta 1',
                pub_date='2024-01-01T00:00:00-06'
            )
        )
        cls.choice = cls.question.choice_set.create(
            choice_text='opcion 1',
        )
        cls.other_question = (
            Question.objects
            .create(
                question_text='pregunta 2',
                pub_date='2024-01-01T00:00:00-06'
            )
        )
        cls.other_choice = cls.other_question.choice_set.create(
            choice_text='opcion 1b',
        )

    def test_voto(self):
        self.assertEqual(self.choice.votes, 0) # votos iniciales 0
        url_page = reverse('polls:detail', kwargs={'pk': self.question.id})
        id_choice_a_votar = self.choice.id
        form_data = {'choice_text': id_choice_a_votar}
        response = self.client.post(url_page, form_data)
        self.choice.refresh_from_db() # actualizar para obtener el nuevo voto
        self.assertEqual(self.choice.votes, 1) # al votar una vez se aumenta
        self.assertEqual(response.status_code, 302) # y redirecciona
        self.assertEqual(response.headers['Location'], reverse('polls:results', kwargs={'pk': self.question.id})) # a esta url

    def test_voto_except(self):
        url_page = reverse('polls:detail', kwargs={'pk': self.question.id})
        id_choice_a_votar = self.other_choice.id
        form_data = {'choice_text': id_choice_a_votar}
        response = self.client.post(url_page, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('errorlist', response.content.decode('utf-8'))


class AjaxTests(APITestCase):
    def test_get(self):
        endpoint = reverse('polls:ajax')
        response = self.client.get(endpoint)
        self.assertEqual(response.data, {'hola': 'mundo'})
        self.assertEqual(response.status_code, 200)

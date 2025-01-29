from django.db.transaction import atomic
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from rest_framework import generics

from .forms import (
    FormAnswers,
    FormQuestion,
)
from .models import Question
from .serializers import HolaSerializer


class AddViewNRequestToContextFormMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(context={'view': self, 'request': self.request})
        return kwargs


class Me(generic.TemplateView):
    template_name = 'polls/me.html'


@method_decorator(
    [atomic],
    'post'
)
class QuestionListCreateIndexView(generic.CreateView):
    template_name = 'polls/index.html'
    form_class = FormQuestion
    success_url = reverse_lazy('polls:index')

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        latest_question_list = (
            Question.objects.order_by('-pub_date')[:5]
        )
        context.update(latest_question_list=latest_question_list)
        return context


@method_decorator(
    [atomic],
    'post'
)
class QuestionDetailView(AddViewNRequestToContextFormMixin, generic.CreateView):
    model = Question
    template_name = 'polls/detail.html'
    form_class = FormAnswers

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context.update(question=self.get_object())
        return context

    def get_success_url(self):
        return reverse_lazy('polls:results', kwargs=self.kwargs)


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    context_object_name = 'question'


class AjaxView(generics.RetrieveAPIView):
    serializer_class = HolaSerializer

    def get_object(self):
        return {'hola': 'mundo'}

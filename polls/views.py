from django.http import JsonResponse
from django.db.transaction import atomic
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from .models import Question
from .forms import (
    FormAnswers,
    FormQuestion,
)


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


class AjaxView(generic.DetailView):
    response_class = JsonResponse
    content_type = 'application/json'

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault("content_type", self.content_type)
        return self.response_class(
            data=context,
            **response_kwargs,
        )

    def get(self, request, *args, **kwargs):
        context = {'hola': 'mundo'}
        return self.render_to_response(context)

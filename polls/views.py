from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.middleware.csrf import get_token
from django.shortcuts import render, get_object_or_404
from django.template import Template, Context
from django.template.loader import get_template
from django.urls import reverse
from django.utils.timezone import now

from .models import Question
from .forms import FormQuestion


def me(request):
    template_name = 'me.html'
    paths = [settings.BASE_DIR/'polls', settings.BASE_DIR/'polls/templates/polls']
    template_exists = False
    for path in paths:
        location = path/template_name
        if location.exists():
            template_exists = True
            break
    if not template_exists:
        return HttpResponse('no había template y sólo pudimos mostrar esto')
    else:
        template = Template('')
        with location.open('r') as archivo_template:
            text_template = archivo_template.read()
            template = Template(text_template)
        context = {}
        return HttpResponse(template.render(Context(context)))


def all_migthy_method(request, pk=None):
    if request.method == 'GET' and pk is None: # list
        template = get_template('polls/index.html') # pudo ser cualquier string
        context = {
            'latest_question_list': Question.objects.order_by("-pub_date")[:5],
            'form': FormQuestion(),
            'csrf_token': get_token(request) # manual
        }
        return HttpResponse(template.render(context))
    if request.method == 'GET' and pk: # retrieve
        context = {'question': get_object_or_404(Question, pk=pk)}
        return render(request, 'polls/detail.html', context)
    if request.method == 'POST': # create
        form = FormQuestion(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.pub_date = now()
            question.save()
            question.choice_set.create(choice_text='yes')
            question.choice_set.create(choice_text='no')
            return HttpResponseRedirect(reverse('polls:index'))
        else:
            context = {
                'latest_question_list': Question.objects.order_by("-pub_date")[:5],
                'form': form,
            }
            return render(request, 'polls/index.html', context) # csrf_token agregado por esta funcion


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
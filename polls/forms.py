# polls/forms.py
from django import forms
from django.utils.translation import gettext_lazy as _

from .choice_service import Vote
from .models import Question
from .question_service import CreateQuestion


class ExtendFormContextMixin:
    def __init__(self, **kwargs):
        self.context = kwargs.pop('context', {})
        super().__init__(**kwargs)


class PostInitFormMixin:
    '''ideal para modificar propiedades de los campos sin reescribir __init__
    no user super o recibirás la excepción'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._post_init()

    def _post_init(self):
        raise NotImplementedError(
            'Subclasses of PostInitFormMixin must provide a _post_init() method.'
        )


class FormQuestion(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']
        labels = {
            'question_text': _('Question'),
        }
        help_texts = {
            'question_text': _('Write the question that you want to make a new poll'),
        }
        error_messages = {
            'question_text': {
                'max_length': _('Question is too long.'),
            },
        }

    def save(self, commit=True):
        data = self.cleaned_data
        # aqui podrías añadir la data del url si es que existe dentro de data y pasarla al negocio
        # por ejemplo:
        # pk = self.context.get('request').parser_context.get('kwargs').get('pk')
        # data.update({'pk'}: pk)
        create_question_service = CreateQuestion(**data)
        return create_question_service.execute() # y esta función deberá regresar un objeto que se alinee a lo que el serializador pida


class FormAnswers(ExtendFormContextMixin, PostInitFormMixin, forms.ModelForm):
    choice_text: forms.ModelChoiceField = forms.ModelChoiceField(
        queryset = None,
        empty_label=None,
        widget=forms.RadioSelect
    )

    class Meta:
        model = Question
        fields = ('choice_text',)

    def _post_init(self):
        question = self.context['view'].get_object()
        if question:
            self.fields['choice_text'].label = question.question_text
            self.fields['choice_text'].queryset = question.choice_set.all()

    def save(self, commit=True):
        vote_service = Vote(self.cleaned_data)
        return vote_service.execute()

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Question


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

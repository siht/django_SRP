# polls/serializers.py
from rest_framework import serializers

from .choice_service import (
    create_choice_service,
    ChoiceCreateDTO,
)
from .models import Choice


class HolaSerializer(serializers.Serializer):
    hola = serializers.CharField()


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('choice_text',)

    def create(self, validated_data):
        question_id = self.context.get('request').parser_context.get('kwargs').get('pk')
        validated_data.update(question_id=question_id)
        choice_dto = ChoiceCreateDTO(question_id=question_id, text=validated_data['choice_text'], votes=None)
        _create_choice_service = create_choice_service(choice_dto)
        choice_dto = _create_choice_service.execute()
        choice_dto.choice_text = choice_dto.text
        return choice_dto

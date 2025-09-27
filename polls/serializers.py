# polls/serializers.py
from rest_framework import serializers

from business_logic.dtos import ChoiceDTO
from business_logic.use_cases import CreateChoice

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
        _create_choice_service = CreateChoice()
        choice_dto = ChoiceDTO(question_id=question_id, text=validated_data['choice_text'])
        choice_dto = _create_choice_service.execute(choice_dto)
        choice_dto.choice_text = choice_dto.text
        return choice_dto

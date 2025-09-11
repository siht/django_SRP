# polls/serializers.py
from rest_framework import serializers

from .choice_service import CreateChoice
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
        create_choice_service = CreateChoice(**validated_data)
        return create_choice_service.execute()

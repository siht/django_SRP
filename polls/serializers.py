from rest_framework import serializers

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
        return super().create(validated_data)

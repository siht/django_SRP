from rest_framework import serializers

class HolaSerializer(serializers.Serializer):
    hola = serializers.CharField()

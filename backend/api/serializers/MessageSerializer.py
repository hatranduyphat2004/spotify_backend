from rest_framework import serializers
from api.models.Message import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

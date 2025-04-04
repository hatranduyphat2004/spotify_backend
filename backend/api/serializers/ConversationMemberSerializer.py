from rest_framework import serializers
from api.models.ConversationMember import ConversationMember

class ConversationMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationMember
        fields = '__all__'

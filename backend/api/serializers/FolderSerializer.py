from rest_framework import serializers
from api.models.Folder import Folder

class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'

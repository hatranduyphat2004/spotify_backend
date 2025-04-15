from rest_framework import serializers
from api.models.Folder import Folder
<<<<<<< HEAD

class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'
=======
from api.serializers.UserSerializer import UserSerializer


class FolderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Folder
        fields = "__all__"
>>>>>>> a3a374d949272e750d165ac423921faeb5a6ae35

from django.db import models
from .User import User


class Folder(models.Model):
    folder_id = models.AutoField(primary_key=True)
    title = models.TextField(max_length=255, default="Untitled")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
<<<<<<< HEAD
    
    class Meta:
        db_table = 'folder'
=======
>>>>>>> a3a374d949272e750d165ac423921faeb5a6ae35

    def __str__(self):
        return f"Folder {self.folder_id} of {self.user.username}"

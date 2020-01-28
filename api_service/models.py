from django.db import models
from django.contrib.auth.models import User


class PictureModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    file = models.FileField(upload_to='profile-pictures/', null=False, blank=False)

    def __str__(self):
        return f'{self.user.email} - {self.file.name}'
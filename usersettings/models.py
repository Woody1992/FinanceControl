from django.contrib.auth.models import User
from django.db import models


class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    currency = models.CharField(max_length=55, blank=True, null=True)

    def __str__(self):
        return str(self.user)+'s' + ' preferences'
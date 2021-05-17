from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class Incomes(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=25)
    date = models.DateField(default=now)
    description = models.CharField(max_length=600, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=255)

    def __str__(self):
        return self.source

    class Meta:
        ordering = ('-date',)


class Source(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


from django.db import models
from django.contrib.auth.models import User
from banque.models import Compte

# Create your models here.

class Signaler(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    compte = models.ForeignKey(Compte, on_delete=models.CASCADE)
    nombre = models.IntegerField()

    class Meta:
        verbose_name = 'Signaler'
        verbose_name_plural = 'Signalers'
from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.


class Entreprise(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nom_entreprise = models.CharField(max_length=150)
    description = models.TextField(("Description de l'entreprise"))
    logo = models.ImageField()
    pays = models.CharField(max_length=50)
    ville = models.CharField(max_length=50)
    numero = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    secteur_activiter = models.CharField(max_length=150)
    is_activate = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)
    supprime = models.BooleanField(default=False)
    date_modification = models.DateTimeField(auto_now=False, auto_now_add=True)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Entreprise'
        verbose_name_plural = 'Entreprises'




class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
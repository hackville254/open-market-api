from django.db import models
from django.contrib.auth.models import User
import uuid
from shortuuid.django_fields import ShortUUIDField

# Create your models here.


class Entreprise(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nom_entreprise = models.CharField(max_length=150)
    devise = models.CharField(max_length=10 , default = "XAF")
    slug = ShortUUIDField(length=5, max_length=5, alphabet="abcdefghijklmnopqrstuvwxyz0123456789", unique=True, editable=False)
    description = models.TextField(("Description de l'entreprise"))
    logo = models.ImageField(upload_to='logo_entreprise')
    pays = models.CharField(max_length=50)
    ville = models.CharField(max_length=50)
    numero = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    secteur_activiter = models.CharField(max_length=150)
    is_activate = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)
    supprime = models.BooleanField(default=False)
    stokage = models.FloatField(default=50)
    espace_disponible = models.FloatField(default=50)
    date_modification = models.DateTimeField(auto_now=False, auto_now_add=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug
    

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
        
class Licence(models.Model):
    e = models.ForeignKey(Entreprise , on_delete = models.CASCADE)
    type_de_licence = models.CharField(max_length = 15)
    date = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Licence d'utilisation"
        verbose_name_plural = "Licences d'utilisations"
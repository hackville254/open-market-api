from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import uuid

from authentification.models import Entreprise
from produits.models import Produit

class Compte(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    is_suspended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Redéfinir les relations pour éviter les conflits
    groups = models.ManyToManyField(Group, related_name='comptes', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='comptes', blank=True)

    def __str__(self):
        return self.email


########################################COMMENTAIRE
class Commentaire(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='commentaires')
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name='commentaires')
    utilisateur = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='commentaires')  # Relation avec Compte
    contenu = models.TextField()  # Renommé pour refléter le contenu
    est_cache = models.BooleanField(default=False)
    cree_a = models.DateTimeField(auto_now_add=True)
    mis_a_jour_a = models.DateTimeField(auto_now=True)  # Utilisez auto_now=True pour mettre à jour la date automatiquement

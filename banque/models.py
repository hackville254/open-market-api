from django.db import models
from django.contrib.auth.models import User
from authentification.models import Entreprise




class CompteBancaire(models.Model):
    proprietaire = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    numero_compte = models.CharField(max_length=20)
    solde = models.FloatField()
    bloque = models.BooleanField(default=False)
    date_modification = models.DateTimeField(auto_now=True)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Compte Bancaire'
        verbose_name_plural = 'Comptes Bancaires'


class Transaction(models.Model):
    montant = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    compte_destination = models.ForeignKey(CompteBancaire, related_name='transactions_destination', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'


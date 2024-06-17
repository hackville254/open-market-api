import uuid
from django.db import models
from django.contrib.auth.models import User
from authentification.models import Entreprise
from produits.models import CHECKOUT


class CompteBancaire(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    numero_compte = models.CharField(max_length=25, default="opm3ce1a0610203828460310")
    numero_operateur = models.CharField(max_length=20, default="opm99999999")
    solde = models.FloatField(default=0)
    bloque = models.BooleanField(default=False)
    supprime = models.BooleanField(default=False)
    date_modification = models.DateTimeField(auto_now=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.entreprise.nom_entreprise

    class Meta:
        verbose_name = "Compte Bancaire"
        verbose_name_plural = "Comptes Bancaires"


class Retrait(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    compte = models.ForeignKey(CompteBancaire, on_delete=models.CASCADE)
    montant = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Retrait d'argent"
        verbose_name_plural = "Retrait d'argent"


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    montant = models.FloatField()
    compte_destination = models.ForeignKey(
        CompteBancaire,
        related_name="transactions_destination",
        on_delete=models.CASCADE,
        null=True,
    )
    compte_source = models.ForeignKey(
        CompteBancaire, related_name="transactions_source", on_delete=models.CASCADE
    )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"


class PaiementEchoue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    checkout = models.ForeignKey(CHECKOUT, on_delete=models.CASCADE)
    token = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Paiement Echoues"
        verbose_name_plural = "Paiement Echoue"


class PaiementReussi(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    checkout = models.ForeignKey(CHECKOUT, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Paiements Réussis"
        verbose_name_plural = "Paiements Réussis"


class MargeBrute(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    checkout = models.ForeignKey(CHECKOUT, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Marge brute par paiement"
        verbose_name_plural = "Marge brute par paiement"


class Historique(models.Model):
    montant = models.FloatField(default = 0)
    devise = models.CharField(max_length=10)
    operation = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Historique OPM"
        verbose_name_plural = "Historiques OPM"      
from django.db import models

from authentification.models import Entreprise



class Compte(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    numero_de_compte = models.CharField(max_length=150)
    solde = models.FloatField(("solde du compte de l'entreprise"),default=0)
    operation = models.CharField(("retrait/depot"), max_length=15)
    bloque = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Compte'
        verbose_name_plural = 'Comptes'
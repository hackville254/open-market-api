import uuid
from django.db import models


class Produit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom_produit = models.CharField(max_length=50)
    description = models.TextField()  # richtext
    image_presentation = models.ImageField()
    gratuit = models.BooleanField(default=False)
    prix_produit = models.FloatField()
    prix_produit_promotion = models.FloatField(null=True)
    langue_produit = models.CharField(max_length=25)
    categorie_produit = models.CharField(max_length=150)
    taille_Fichier = models.IntegerField()
    # demo_produit =
    supprime = models.BooleanField(default=False)
    date_modification = models.DateTimeField(auto_now=True)
    date = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = ("Produit")
        verbose_name_plural = ("Produits")

    def __str__(self):
        return self.nom_produit

#image de presentation du produit



class Fichier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    produit = models.ForeignKey(Produit,  on_delete=models.CASCADE)
    fichier = models.FileField()


class ProduitNumerique(Produit):
    type = models.CharField(
        ("Pour specifier le type de document"), max_length=50)

    class Meta:
        verbose_name = 'Produit Numerique'
        verbose_name_plural = 'Produit Numeriques'


class Livre(Produit):
    #auteur = models.CharField(max_length=150)
    nombre_page = models.IntegerField()
    #editeur = models.CharField(max_length=150)

    class Meta:
        verbose_name = 'Livre'
        verbose_name_plural = 'Livres'


class Acce(Produit):  # lien pour acceder a un evenement,une invitation...
    lien = models.URLField(max_length=500)
    delais = models.DateTimeField()

    class Meta:
        verbose_name = 'Acce'
        verbose_name_plural = 'Acces'

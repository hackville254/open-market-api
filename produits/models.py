import uuid
from django.db import models
from django_quill.fields import QuillField
from authentification.models import Entreprise
from shortuuid.django_fields import ShortUUIDField


class Produit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = ShortUUIDField(length=5, max_length=5, alphabet="abcdefghijklmnopqrstuvwxyz0123456789", unique=True, editable=False)
    entreprise = models.ForeignKey(
        Entreprise, on_delete=models.CASCADE, null=True)
    nom_produit = models.CharField(max_length=50)
    description = models.TextField()  # richtext
    image_presentation = models.ImageField()
    gratuit = models.BooleanField(default=False)
    prix_produit = models.FloatField()
    promotion  = models.BooleanField(default=False)
    prix_produit_promotion = models.FloatField(null=True)
    duree_promotion = models.DateTimeField(null=True)
    langue_produit = models.CharField(max_length=25)
    categorie_produit = models.CharField(max_length=150)
    taille_Fichier = models.FloatField(default=0, null=True)
    is_visible = models.BooleanField(default=True)
    # demo_produit =
    supprime = models.BooleanField(default=False)
    date_modification = models.DateTimeField(auto_now=True)
    date = models.DateTimeField(auto_now_add=True)
   
    class Meta:
        verbose_name = "Produit de OPM"
        verbose_name_plural = "Tous les produits de OPM"

    def __str__(self):
        return self.nom_produit

# image de presentation du produit


class Fichier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    produit = models.ForeignKey(Produit,  on_delete=models.CASCADE)
    fichier = models.FileField()


class Visite(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE , null=True)
    ip_client = models.GenericIPAddressField()
    region = models.CharField(max_length=150 , null = True) 
    pays = models.CharField(max_length=150 , null = True) 
    ville = models.CharField(max_length=150, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("Visite")
        verbose_name_plural = ("Visites")

class VisiteMultiple(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, verbose_name="Entreprise")
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, null=True, verbose_name="Produit")
    ip_client = models.GenericIPAddressField(verbose_name="IP Client")
    region = models.CharField(max_length=150, null=True, verbose_name="Région")
    pays = models.CharField(max_length=150, null=True, verbose_name="Pays")
    ville = models.CharField(max_length=150, null=True, verbose_name="Ville")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date de Visite")

    class Meta:
        verbose_name = "Visite Multiple"
        verbose_name_plural = "Visites Multiples"


class ProduitNumerique(Produit):
    type = models.CharField(
        ("Pour specifier le type de document"), max_length=50)

    class Meta:
        verbose_name = 'Produit Numerique'
        verbose_name_plural = 'Produit Numeriques'


class Livre(Produit):
    # auteur = models.CharField(max_length=150)
    nombre_page = models.IntegerField(null=True)
    # editeur = models.CharField(max_length=150)

    class Meta:
        verbose_name = 'Livre'
        verbose_name_plural = 'Livres'


class Acce(Produit):  # lien pour acceder a un evenement,une invitation...
    lien = models.URLField(max_length=500)
    #delais = models.DateTimeField() #Delais de validiter du lien
    class Meta:
        verbose_name = 'Acce'
        verbose_name_plural = 'Acces'


class CHECKOUT(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.CharField(max_length = 100 ,null = True)
    slug = ShortUUIDField(length=10, max_length=10, alphabet="abcdefghijklmnopqrstuvwxyz0123456789", unique=True, editable=False)
    produit = models.ForeignKey(Produit , on_delete=models.CASCADE , null = True)
    prix_produit = models.FloatField(default=0)  # Nouveau champ pour le prix du produit
    taux = models.FloatField(default=10.0)  # Nouveau champ pour le taux par défaut
    prix_client = models.FloatField(default=0)  # Nouveau champ pour le prix que le client paye
    entreprise = models.ForeignKey(Entreprise , on_delete=models.CASCADE)
    nom_client = models.CharField(max_length = 100)
    devise_client = models.CharField(max_length = 5)
    status = models.CharField(max_length = 20 , default = 'initialiser')
    type = models.CharField(max_length = 10 , default = "Achat")
    pays_client = models.CharField(max_length = 50)
    moyen_de_paiement = models.CharField(max_length = 50)
    numero = models.CharField(max_length = 30 , null = True)
    email = models.CharField(max_length = 30 , null = True)
    codeOtp = models.CharField(max_length = 10 , null = True)
    orderId = models.CharField(max_length = 10 , null = True, default = "open_market")
    date = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.entreprise.nom_entreprise


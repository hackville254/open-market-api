import uuid
from django.db import models

from authentification.models import Entreprise
from produits.models import Produit



class FacebookPixel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entreprise = models.ForeignKey(
        Entreprise, on_delete=models.CASCADE, null=True)
    produit = models.ForeignKey(Produit,  on_delete=models.CASCADE)
    pixel_id = models.CharField(max_length=16)
    date = models.DateTimeField(auto_now_add=True)
    
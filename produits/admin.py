from django.contrib import admin
from .models import Livre, ProduitNumerique
# Register your models here.

from django.contrib import admin
from .models import Produit

class ProduitNumeriqueAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom_produit', 'gratuit', 'prix_produit', 'langue_produit', 'categorie_produit','supprime', 'date_modification', 'date')
    list_display_links = ('id', 'nom_produit')  # Les champs cliquables pour accéder à la modification

class LivreAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom_produit', 'gratuit', 'prix_produit', 'langue_produit', 'categorie_produit','supprime', 'date_modification', 'date')
    list_display_links = ('id', 'nom_produit')  # Les champs cliquables pour accéder à la modification




admin.site.register(ProduitNumerique, ProduitNumeriqueAdmin)
admin.site.register(Livre, LivreAdmin)







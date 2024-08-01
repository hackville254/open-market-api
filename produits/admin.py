from django.contrib import admin
from .models import CHECKOUT, Fichier, Livre, ProduitNumerique, Acce, Visite

# Register your models here.

from django.contrib import admin

class ProduitNumeriqueAdmin(admin.ModelAdmin):
    list_display = ('slug', 'nom_produit', 'gratuit', 'prix_produit', 'langue_produit', 'categorie_produit','supprime', 'date_modification', 'date')
    list_display_links = ('slug', 'nom_produit')  # Les champs cliquables pour accéder à la modification
    ordering = ('-date',)  # Afficher les plus récents en premier

class LivreAdmin(admin.ModelAdmin):
    list_display = ('slug', 'nom_produit', 'gratuit', 'prix_produit', 'langue_produit', 'categorie_produit','supprime', 'date_modification', 'date')
    list_display_links = ('slug', 'nom_produit')  # Les champs cliquables pour accéder à la modification
    ordering = ('-date',)  # Afficher les plus récents en premier

class AcceAdmin(admin.ModelAdmin):
    list_display = ('slug', 'nom_produit', 'gratuit', 'prix_produit', 'langue_produit', 'categorie_produit','supprime', 'date_modification', 'date')
    list_display_links = ('slug', 'nom_produit')  # Les champs cliquables pour accéder à la modification
    ordering = ('-date',)  # Afficher les plus récents en premier


class CHECKOUTAdmin(admin.ModelAdmin):
    list_display = ('entreprise','produit', 'nom_client', 'status', 'pays_client', 'email','moyen_de_paiement', 'numero', 'date_modification', 'date')
    list_display_links = ('entreprise','produit')  # Les champs cliquables pour accéder à la modification
    search_fields = ('reference', 'nom_client', 'status', 'type', 'pays_client', 'moyen_de_paiement', 'numero', 'email')
    list_filter = ('status', 'type', 'pays_client', 'moyen_de_paiement', 'date')
    ordering = ('-date',)  # Afficher les plus récents en premier


class FichierAdmin(admin.ModelAdmin):
    list_display = ('produit',)


class VisiteAdmin(admin.ModelAdmin):
    list_display = ("entreprise", "ip_client", "date")
    search_fields = ("entreprise__nom_entreprise",)
    list_filter = ("date", "entreprise")
    date_hierarchy = "date"


admin.site.register(Visite, VisiteAdmin)
admin.site.register(CHECKOUT, CHECKOUTAdmin)
admin.site.register(ProduitNumerique, ProduitNumeriqueAdmin)
admin.site.register(Livre, LivreAdmin)
admin.site.register(Acce, AcceAdmin)
admin.site.register(Fichier,FichierAdmin)

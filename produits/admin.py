from django.contrib import admin
from .models import CHECKOUT,Fichier,Livre, ProduitNumerique,Acce,VisiteAcces,VisiteLivre,VisiteProduitNumerique
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
    list_display = ('slug', 'reference', 'produit', 'entreprise', 'nom_client', 'status', 'type', 'pays_client', 'moyen_de_paiement', 'numero', 'email', 'date_modification', 'date')
    list_display_links = ('slug', 'reference')  # Les champs cliquables pour accéder à la modification
    search_fields = ('reference', 'nom_client', 'status', 'type', 'pays_client', 'moyen_de_paiement', 'numero', 'email')
    list_filter = ('status', 'type', 'pays_client', 'moyen_de_paiement', 'date')
    ordering = ('-date',)  # Afficher les plus récents en premier


class FichierAdmin(admin.ModelAdmin):
    list_display = ('produit',)

admin.site.register(CHECKOUT , CHECKOUTAdmin)
admin.site.register(ProduitNumerique, ProduitNumeriqueAdmin)
admin.site.register(Livre, LivreAdmin)
admin.site.register(Acce, AcceAdmin)
admin.site.register(VisiteAcces)
admin.site.register(VisiteLivre)    
admin.site.register(VisiteProduitNumerique)
admin.site.register(Fichier,FichierAdmin)
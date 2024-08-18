from django.contrib import admin
from .models import CHECKOUT, Fichier, Livre, ProduitNumerique, Acce,Visite
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


@admin.register(Visite)
class VisiteAdmin(admin.ModelAdmin):
    # Champs à afficher dans la liste des objets
    list_display = ('entreprise', 'produit', 'ip_client', 'region', 'pays', 'ville', 'date')

    # Champs par lesquels trier les objets dans la liste
    ordering = ('-date',)  # Trie par date décroissante

    # Champs filtrables dans la barre latérale de l'administration
    list_filter = ('entreprise', 'produit', 'region', 'pays', 'ville')

    # Champs recherchables
    search_fields = ('ip_client', 'region', 'pays', 'ville')

    # Champs pour les formulaires de création et d'édition
    fieldsets = (
        (None, {
            'fields': ('entreprise', 'produit', 'ip_client', 'region', 'pays', 'ville')
        }),
        ('Date Information', {
            'fields': ('date',),
            'classes': ('collapse',),  # Réduit la section "Date Information" par défaut
        }),
    )

    # Champs de lecture seule
    readonly_fields = ('date',)

admin.site.register(CHECKOUT, CHECKOUTAdmin)
admin.site.register(ProduitNumerique, ProduitNumeriqueAdmin)
admin.site.register(Livre, LivreAdmin)
admin.site.register(Acce, AcceAdmin)
admin.site.register(Fichier,FichierAdmin)



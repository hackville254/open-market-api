from django.contrib import admin
from .models import CHECKOUT, Fichier, Livre, ProduitNumerique, Acce,Visite,Produit, VisiteMultiple
# Register your models here.

from django.contrib import admin

@admin.register(VisiteMultiple)
class VisiteMultipleAdmin(admin.ModelAdmin):
    list_display = ('entreprise', 'produit', 'ip_client', 'region', 'pays', 'ville', 'date')
    list_filter = ('entreprise', 'produit', 'date')
    search_fields = ('ip_client', 'region', 'pays', 'ville')
    date_hierarchy = 'date'
    ordering = ('-date',)
    verbose_name = "Visite Multiple"
    verbose_name_plural = "Visites Multiples"


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
    list_display = (
        'entreprise', 'produit', 'nom_client','prix_produit', 'prix_client','taux_affiche' , 'status', 'pays_client', 
        'email', 'moyen_de_paiement', 'numero', 'date_modification', 'date'
    )
    list_display_links = ('entreprise', 'produit')  # Champs cliquables pour accéder à la modification
    search_fields = (
        'reference', 'nom_client', 'status', 'type', 'pays_client', 
        'moyen_de_paiement', 'numero', 'email'
    )
    list_filter = ('status', 'type', 'pays_client', 'moyen_de_paiement', 'date')
    ordering = ('-date',)  # Afficher les plus récents en premier

    def taux_affiche(self, obj):
        return f"{obj.taux}%"

    taux_affiche.short_description = "Taux (%)"


    actions = ['update_product_and_client_prices']

    def update_product_and_client_prices(self, request, queryset):
        updated_count = 0
        for checkout in queryset:
            if checkout.produit:
                checkout.prix_produit = checkout.produit.prix_produit
                checkout.prix_client = checkout.prix_produit * 1.1  # 10% added to product price
            else:
                checkout.prix_produit = 0
                checkout.prix_client = 0
            checkout.save()
            updated_count += 1
        self.message_user(request, f'{updated_count} checkouts mis à jour avec les prix des produits et les prix des clients.')

    update_product_and_client_prices.short_description = "Mettre à jour les prix des produits et des clients pour les checkouts sélectionnés"



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


class ProduitAdmin(admin.ModelAdmin):
    # Définir les colonnes à afficher dans la liste
    list_display = (
        'nom_produit', 'entreprise', 'prix_produit', 'promotion', 
        'prix_produit_promotion', 'duree_promotion', 'is_visible', 
        'date_modification', 'date'
    )
    # Ajouter des filtres par champ
    list_filter = (
        'entreprise', 'gratuit', 'promotion', 'is_visible', 
        'langue_produit', 'categorie_produit', 'supprime'
    )
    # Ajouter une barre de recherche
    search_fields = ('nom_produit', 'description', 'categorie_produit')
    # Ordre de tri par défaut
    ordering = ('-date_modification',)
    # Ajout de champs non modifiables dans le formulaire
    readonly_fields = ('id', 'slug', 'date_modification', 'date')

    # Affichage détaillé dans le formulaire d'administration
    fieldsets = (
        ('Informations Générales', {
            'fields': ('nom_produit', 'description', 'image_presentation', 'categorie_produit')
        }),
        ('Informations d\'Entreprise', {
            'fields': ('entreprise', 'langue_produit')
        }),
        ('Prix et Promotion', {
            'fields': ('gratuit', 'prix_produit', 'promotion', 'prix_produit_promotion', 'duree_promotion')
        }),
        ('Visibilité et Statut', {
            'fields': ('is_visible', 'supprime')
        }),
        ('Dates', {
            'fields': ('date_modification', 'date')
        }),
    )

# Enregistrer le modèle avec sa classe d'administration personnalisée
admin.site.register(Produit, ProduitAdmin)




admin.site.register(CHECKOUT, CHECKOUTAdmin)
admin.site.register(ProduitNumerique, ProduitNumeriqueAdmin)
admin.site.register(Livre, LivreAdmin)
admin.site.register(Acce, AcceAdmin)
admin.site.register(Fichier,FichierAdmin)



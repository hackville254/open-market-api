from django.contrib import admin
from .models import FacebookPixel

@admin.register(FacebookPixel)
class FacebookPixelAdmin(admin.ModelAdmin):
    # Champs affichés dans la liste
    list_display = ('id', 'entreprise', 'produit', 'pixel_id', 'date')
    # Champs sur lesquels on peut chercher
    search_fields = ('pixel_id', 'entreprise__nom', 'produit__nom')
    # Filtres disponibles pour les colonnes
    list_filter = ('entreprise', 'produit', 'date')
    # Champs en lecture seule
    readonly_fields = ('id', 'date')
    # Ordre par défaut
    ordering = ('-date',)

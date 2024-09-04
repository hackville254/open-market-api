from django.contrib import admin
from .models import Entreprise, Notification

class EntrepriseAdmin(admin.ModelAdmin):
    list_display = (
        'nom_entreprise', 'pays', 'ville', 'numero', 
        'email', 'secteur_activiter', 'is_activate', 'is_private', 
        'supprime', 'date_modification', 'date'
    )
    list_filter = (
        'pays', 'ville', 'is_activate', 'is_private', 'supprime', 
        'secteur_activiter'
    )
    search_fields = ('nom_entreprise', 'description', 'pays', 'ville', 'email', 'secteur_activiter')
    ordering = ('-date_modification',)
    readonly_fields = ('id', 'slug', 'date_modification', 'date')

    fieldsets = (
        ('Informations Générales', {
            'fields': ('slug', 'nom_entreprise', 'description', 'logo')
        }),
        ('Détails de Contact', {
            'fields': ('pays', 'ville', 'numero', 'email')
        }),
        ('Informations de l\'Entreprise', {
            'fields': ('user', 'secteur_activiter', 'devise', 'stokage', 'espace_disponible')
        }),
        ('Statut et Visibilité', {
            'fields': ('is_activate', 'is_private', 'supprime')
        }),
        ('Dates', {
            'fields': ('date_modification', 'date')
        }),
    )

    actions = ['activate_enterprises', 'deactivate_enterprises']

    def activate_enterprises(self, request, queryset):
        """
        Active les entreprises sélectionnées.
        """
        updated_count = queryset.update(is_activate=True)
        names = ', '.join([e.nom_entreprise for e in queryset])
        self.message_user(request, f"{updated_count} entreprises activées : {names}")
    
    activate_enterprises.short_description = "Activer les entreprises sélectionnées"

    def deactivate_enterprises(self, request, queryset):
        """
        Désactive les entreprises sélectionnées.
        """
        updated_count = queryset.update(is_activate=False)
        names = ', '.join([e.nom_entreprise for e in queryset])
        self.message_user(request, f"{updated_count} entreprises désactivées : {names}")

    deactivate_enterprises.short_description = "Désactiver les entreprises sélectionnées"

admin.site.register(Entreprise, EntrepriseAdmin)

from django.contrib import admin
from .models import (
    CompteBancaire,
    Transaction,
    PaiementEchoue,
    PaiementReussi,
    Retrait,
    Historique,
)

# Register your models here.


class PaiementEchoueAdmin(admin.ModelAdmin):
    list_display = ("checkout", "token" ,"date")
    search_fields = ("checkout", )
    list_filter = ("date",)
    ordering = ("-date",)


class PaiementReussiAdmin(admin.ModelAdmin):
    list_display = ("checkout", "date")
    search_fields = ("checkout", "date")
    list_filter = ("checkout", "date")
    ordering = ("-date",)



class RetraitAdmin(admin.ModelAdmin):
    list_display = ("id", "compte", "montant", "date")
    search_fields = ("compte__entreprise",)
    list_filter = ("date",)
    ordering = ("-date",)


class HistoriqueAdmin(admin.ModelAdmin):
    list_display = ("montant", "devise", "operation" , "date")
    list_filter = ("devise","operation","date")
    ordering = ("-date",)


admin.site.register(PaiementEchoue, PaiementEchoueAdmin)
admin.site.register(PaiementReussi, PaiementReussiAdmin)
admin.site.register(Retrait, RetraitAdmin)
admin.site.register(Historique , HistoriqueAdmin)


@admin.register(CompteBancaire)
class CompteBancaireAdmin(admin.ModelAdmin):
    # Liste des champs à afficher dans la liste des comptes bancaires
    list_display = (
        "id",
        "get_nom_entreprise",
        "numero_compte",
        "numero_operateur",
        "solde",
        "bloque",
        "supprime",
        "date_modification",
        "date",
    )
    # Filtres pour la liste des comptes bancaires
    list_filter = ("bloque", "supprime")
    # Champs de recherche pour la liste des comptes bancaires
    search_fields = (
        "id",
        "entreprise__nom_entreprise",
        "numero_compte",
        "numero_operateur",
    )
    # Champs en lecture seule dans le formulaire de modification
    readonly_fields = ("id", "date_modification", "date")
    # Définition des sections dans le formulaire de modification
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "entreprise",
                    "numero_compte",
                    "numero_operateur",
                    "solde",
                    "bloque",
                    "supprime",
                )
            },
        ),
        (
            "Informations de Suivi",
            {
                "fields": ("date_modification", "date"),
                "classes": ("collapse",),
            },
        ),
    )

    def get_nom_entreprise(self, obj):
        return obj.entreprise.nom_entreprise

    get_nom_entreprise.short_description = "Nom de l'entreprise"

    ordering = ("-date",)
    
    # Actions personnalisées
    actions = ['block_accounts', 'unblock_accounts']

    def block_accounts(self, request, queryset):
        """
        Bloque les comptes bancaires sélectionnés.
        """
        updated_count = queryset.update(bloque=True)
        self.message_user(request, f"{updated_count} comptes bancaires bloqués.")

    block_accounts.short_description = "Bloquer les comptes bancaires sélectionnés"

    def unblock_accounts(self, request, queryset):
        """
        Débloque les comptes bancaires sélectionnés.
        """
        updated_count = queryset.update(bloque=False)
        self.message_user(request, f"{updated_count} comptes bancaires débloqués.")

    unblock_accounts.short_description = "Débloquer les comptes bancaires sélectionnés"


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "montant",
        "compte_source",
        "compte_destination",
        "date",
    )
    list_filter = ("user", "date")
    search_fields = (
        "id",
        "user__username",
        "compte_source__numero_compte",
        "compte_destination__numero_compte",
    )
    readonly_fields = ("id", "date")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "user",
                    "montant",
                    "compte_source",
                    "compte_destination",
                )
            },
        ),
        (
            "Informations supplémentaires",
            {
                "fields": ("date",),
                "classes": ("collapse",),
            },
        ),
    )
    ordering = ("-date",)

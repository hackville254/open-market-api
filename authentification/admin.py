from django.contrib import admin
from .models import Entreprise,Notification
# Register your models here.

class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ('slug', 'nom_entreprise', 'pays', 'ville', 'numero', 'date_modification', 'date')
    list_display_links = ('slug', 'nom_entreprise')  # Les champs cliquables pour accéder à la modification




admin.site.register(Entreprise , EntrepriseAdmin)


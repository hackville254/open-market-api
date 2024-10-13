from django.contrib import admin
from .models import Compte

@admin.register(Compte)
class CompteAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'is_suspended', 'created_at')
    search_fields = ('email',)

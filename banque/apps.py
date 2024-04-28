from django.apps import AppConfig


class BanqueConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'banque'
    def ready(self):
        import banque.signals  # Importer les signaux
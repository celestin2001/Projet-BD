# gestion_content/apps.py
from django.apps import AppConfig

class GestionContentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestion_content'

    def ready(self):
        import gestion_content.signals # Importation importante
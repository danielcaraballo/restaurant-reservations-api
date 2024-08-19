from django.apps import AppConfig
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

class GestionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.gestion'

    def ready(self):
        # Importa el modelo y el receptor de señales aquí para evitar errores de importación circular
        from apps.gestion import signals
from django.apps import AppConfig


class SigelinConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sigelin'

class SigelinConfig(AppConfig):
    name = 'sigelin'

    def ready(self):
        import sigelin.signals


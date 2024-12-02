from django.apps import AppConfig


class PhonesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'phones'

    def ready(self):
        import phones.signals

from django.apps import AppConfig


class DiLoaderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'di_loader'

    def ready(self):
        from . import production_builder
        production_builder.main()

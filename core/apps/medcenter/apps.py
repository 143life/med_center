from django.apps import AppConfig


class MedcenterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core.apps.medcenter"
    verbose_name = "Медицинский центр"

    def ready(self):
        import core.apps.medcenter.ws.signals  # noqa

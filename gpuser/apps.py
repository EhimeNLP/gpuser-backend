from django.apps import AppConfig


class GpuserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gpuser"

    def ready(self) -> None:
        from .ap_scheduler import start

        start()

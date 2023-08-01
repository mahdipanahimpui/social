from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'

    # to declare signals.py  override the ready function
    def ready(self):
        from . import signals

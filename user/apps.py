from django.apps import AppConfig
from django.db.models.signals import post_migrate

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        from . import signals  # signals.py에서 처리
        post_migrate.connect(signals.create_default_stacks, sender=self)
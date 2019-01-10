from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'apps.accounts'

    def ready(self):
        from django.contrib.auth.models import User

        try:
            User.objects.get(username="system_user")

        except User.DoesNotExist:
            User.objects.create_user(username="system_user", password="system_user")

from django.apps import AppConfig


class ManageUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'manage_users'

    def ready(self):
        import manage_users.signals

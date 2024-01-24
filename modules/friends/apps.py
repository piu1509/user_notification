from django.apps import AppConfig


class FriendsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.friends'

    def ready(self):
        import modules.friends.signals

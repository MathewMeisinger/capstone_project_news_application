from django.apps import AppConfig


class UsersConfig(AppConfig):
    """ Configuration for the users application."""
    name = 'users'

    def ready(self):
        import users.signals

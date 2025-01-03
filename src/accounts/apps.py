from django.apps import AppConfig


class AccountsConfig(AppConfig):  # Use the correct class name
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'  # Ensure this matches your app folder name

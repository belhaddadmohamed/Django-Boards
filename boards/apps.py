from django.apps import AppConfig

class BoardsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "boards"

# DjangoSuit Configurations
# web site link : https://django-suit.readthedocs.io/en/v2/install.html
# from suit.apps import DjangoSuitConfig
# class SuitConfig(DjangoSuitConfig):
#     layout = 'horizontal'

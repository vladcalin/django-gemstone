from django.apps import AppConfig, apps
from django.utils.module_loading import import_module


class DjangoGemstoneConfig(AppConfig):
    name = 'django_gemstone'

    def ready(self):
        for app_config in apps.get_app_configs():
            module = app_config.module

            methods = module.__name__ + ".methods"
            try:
                import_module(methods)
            except ModuleNotFoundError:
                pass

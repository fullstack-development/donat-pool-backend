from django.apps import AppConfig


class FundraisingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'donat_pool.fundraising'

    def ready(self):
        import donat_pool.fundraising.signals

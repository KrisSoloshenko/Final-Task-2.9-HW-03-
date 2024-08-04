from django.apps import AppConfig
from django.db.models.signals import m2m_changed



class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'
    def ready(self):
        from . import signals
        m2m_changed.connect(signals.post_category_created)


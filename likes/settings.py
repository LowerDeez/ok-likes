from django.conf import settings as django_setting

__all__ = (
    'LIKES_MODELS',
)


LIKES_MODELS = getattr(django_setting, 'LIKES_MODELS', {})

from django.conf import settings as django_setting

__all__ = (
    'LIKES_MODELS',
    'LIKES_REST_PAGINATION_CLASS'
)


LIKES_MODELS = getattr(django_setting, 'LIKES_MODELS', {})
LIKES_REST_PAGINATION_CLASS = getattr(
    django_setting,
    'LIKES_REST_PAGINATION_CLASS',
    None
)

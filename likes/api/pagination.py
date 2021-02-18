from django.utils.module_loading import import_string

from rest_framework.settings import api_settings

from likes.settings import LIKES_REST_PAGINATION_CLASS

__all__ = (
    'get_pagination_class',
)


def get_pagination_class():
    """
    Returns custom pagination class, set in settings
    """
    pagination_class = LIKES_REST_PAGINATION_CLASS

    if pagination_class:
        try:
            return import_string(pagination_class)
        except ImportError:
            pass

    return api_settings.DEFAULT_PAGINATION_CLASS

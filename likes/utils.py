from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from likes.settings import LIKES_MODELS

__all__ = (
    'allowed_content_type',
    'admin_change_url'
)

User = get_user_model()


def allowed_content_type(ct: ContentType) -> bool:
    name = f'{ct.app_label}.{ct.model.title()}'
    if name in LIKES_MODELS.keys():
        return True
    return False


def admin_change_url(obj) -> str:
    """
    Returns admin change url for a given object.
    """
    app_label = obj._meta.app_label
    model_name = obj._meta.model.__name__.lower()
    return reverse(
        f'admin:{app_label}_{model_name}_change',
        args=(obj.pk,)
    )

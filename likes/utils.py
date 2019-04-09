from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.http.request import HttpRequest
from django.urls import reverse

from .models import Like
from .settings import LIKES_MODELS
from .signals import object_liked, object_unliked

__all__ = (
    'allowed_content_type',
    'admin_change_url',
    'send_signals'
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


def send_signals(
        created: bool,
        request: HttpRequest,
        like: Like,
        obj
):
    """
    Sends signals when object was liked and unliked.
    """
    if created:
        object_liked.send(
            sender=Like,
            like=like,
            request=request
        )
    else:
        object_unliked.send(
            sender=Like,
            object=obj,
            request=request
        )

from typing import TYPE_CHECKING, Tuple

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.http import HttpRequest

from likes.models import Like
from likes.signals import object_liked, object_unliked
from likes.selectors import get_user_likes

if TYPE_CHECKING:
    from django.db.models import Model

User = get_user_model()

__all__ = (
    'toggle',
    'get_user_likes_count',
    'get_object_likes_count',
    'is_object_liked_by_user',
    'send_signals'
)


def toggle(
        *,
        user: 'User',
        content_type: 'ContentType',
        object_id: str
) -> Tuple['Like', bool]:
    """
    Class method to like-dislike object
    """
    obj, created = Like.objects.get_or_create(
        sender=user,
        content_type=content_type,
        object_id=object_id
    )

    if not created:
        obj.delete()

    return obj, created


def get_user_likes_count(
        *,
        user: 'User',
        content_type: 'ContentType' = None
) -> int:
    """
    Returns count of likes for a given user.
    """
    if not user.is_authenticated:
        return 0

    return (
        get_user_likes(
            user=user,
            content_type=content_type
        )
        .count()
    )


def get_object_likes_count(*, obj: 'Model') -> int:
    """
    Returns count of likes for a given object.
    """
    return (
        Like.objects
        .filter(
            content_type=(
                ContentType.objects.get_for_model(obj)
            ),
            object_id=obj.pk
        )
        .count()
    )


def is_object_liked_by_user(
        *,
        obj: 'Model',
        user: 'User'
) -> bool:
    """
    Checks if a given object is liked by a given user.
    """
    if not user.is_authenticated:
        return False

    return (
        Like.objects
        .filter(
            content_type=(
                ContentType.objects.get_for_model(obj)
            ),
            object_id=obj.pk,
            sender=user
        )
        .exists()
    )


def send_signals(
        *,
        created: bool,
        request: HttpRequest,
        like: 'Like',
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

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from likes.models import Like

__all__ = (
    'user_likes_count',
    'obj_likes_count',
    'is_liked',
    'get_who_liked'
)

User = get_user_model()


def user_likes_count(user: User) -> int:
    """
    Returns count of likes for a given user.
    """
    if not user.is_authenticated:
        return 0
    return (
        Like.objects
        .filter(
            sender=user,
            content_type__isnull=False,
            object_id__isnull=False
        )
        .count()
    )


def obj_likes_count(obj) -> int:
    """
    Returns count of likes for a given object.
    """
    return (
        Like.objects
        .filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.pk
        )
        .count()
    )


def is_liked(obj, user: User) -> bool:
    """
    Checks if a given object is liked by a given user.
    """
    if not user.is_authenticated:
        return False
    ct = ContentType.objects.get_for_model(obj)
    return (
        Like.objects
        .filter(
            content_type=ct,
            object_id=obj.pk,
            sender=user
        )
        .exists()
    )


def get_who_liked(obj):
    """
    Returns users, who liked a given object.
    """
    ct = ContentType.objects.get_for_model(obj)
    return (
        User.objects
        .filter(
            likes__content_type=ct,
            likes__object_id=obj.pk
        )
    )

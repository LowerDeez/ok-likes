from typing import List, TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from .models import Like

if TYPE_CHECKING:
    from django.db.models import QuerySet, Model

User = get_user_model()

__all__ = (
    'get_user_likes',
    'get_liked_object_ids',
    'get_users_who_liked_object'
)


def get_user_likes(
        *,
        user: 'User',
        content_type: 'ContentType' = None
) -> 'QuerySet':
    queryset = Like.objects.filter(sender=user)

    if content_type:
        queryset = queryset.filter(content_type=content_type)

    return queryset


def get_liked_object_ids(
        *,
        user: 'User',
        content_type: 'ContentType' = None
) -> List[str]:
    if not user.is_authenticated:
        return []

    queryset = get_user_likes(
        user=user,
        content_type=content_type
    )

    ids = queryset.values_list('object_id', flat=True)

    return list(set(ids))


def get_users_who_liked_object(*, obj: 'Model'):
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

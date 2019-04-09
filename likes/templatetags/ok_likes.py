from django.db.models import QuerySet
from django.template import Library

from ..models import Like
from likes.services import (
    obj_likes_count,
    is_liked as is_liked_util,
    get_who_liked
)

register = Library()

__all__ = (
    'likes_count',
    'who_liked',
    'likes',
    'is_liked'
)


@register.simple_tag
@register.filter
def likes_count(obj) -> int:
    """
    Returns count of likes for a given object

    Usage:
        {% likes_count obj %}
    or
        {% likes_count obj as var %}
    or
        {{ obj|likes_count }}
    """
    return obj_likes_count(obj)


@register.simple_tag
def who_liked(obj) -> QuerySet:
    """
    Returns users, who liked a given object.

    Usage:
        {% who_liked object as fans %}
    """
    return get_who_liked(obj)


@register.simple_tag
def likes(user) -> QuerySet:
    """
    Returns likes for a given user

    Usage:
        {% likes request.user as var %}
    """
    return Like.objects.filter(sender=user)


@register.simple_tag
def is_liked(obj, user) -> bool:
    """
    Checks if a given object liked by a given user.

    Usage:
        {% is_liked object request.user as var %}
    """
    return is_liked_util(obj, user)

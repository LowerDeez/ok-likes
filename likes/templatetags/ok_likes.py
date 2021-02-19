from django.db.models import QuerySet
from django.template import Library

from ..models import Like
from likes.services import (
    get_object_likes_count,
    is_object_liked_by_user as is_liked_util
)
from ..selectors import get_users_who_liked_object, get_user_likes

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
    return get_object_likes_count(obj=obj)


@register.simple_tag
def who_liked(obj) -> QuerySet:
    """
    Returns users, who liked a given object.

    Usage:
        {% who_liked object as fans %}
    """
    return get_users_who_liked_object(obj=obj)


@register.simple_tag
def likes(user) -> QuerySet:
    """
    Returns likes for a given user

    Usage:
        {% likes request.user as var %}
    """
    return get_user_likes(user=user)


@register.simple_tag
def is_liked(obj, user) -> bool:
    """
    Checks if a given object liked by a given user.

    Usage:
        {% is_liked object request.user as var %}
    """
    return is_liked_util(obj=obj, user=user)

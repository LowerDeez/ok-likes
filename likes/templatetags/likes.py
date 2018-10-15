from django.db.models import QuerySet
from django.template import Library

from ..models import Like
from ..utils import get_who_liked, obj_likes_count

register = Library()

__all__ = (
    'who_liked',
    'likes_count',
    'likes'
)


@register.simple_tag
def who_liked(obj) -> QuerySet:
    """
    Return users, who liked given object.

    Usage:
        {% who_liked object as fans %}
    """
    return get_who_liked(obj)


@register.simple_tag
@register.filter
def likes_count(obj):
    """
    Return count of likes for given object

    Usage:
        {% likes_count obj %}
    or
        {% likes_count obj as var %}
    or
        {{ obj|likes_count }}
    """
    return obj_likes_count(obj)


@register.simple_tag
def likes(user):
    """
    Return likes for current user

    Usage:
        {% likes request.user as var %}
    """
    return Like.objects.filter(sender=user)

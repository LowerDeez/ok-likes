from django.apps import apps


if apps.is_installed('django_jinja'):

    from django.db.models import QuerySet

    from django_jinja import library

    from ..models import Like
    from ..utils import get_who_liked as who_liked, obj_likes_count

    __all__ = (
        'get_who_liked',
        'get_likes_count',
        'get_likes'
    )

    @library.global_function
    def get_who_liked(obj) -> QuerySet:
        """
        Return users, who liked given object.

        Usage:
            {{ get_who_liked(object) }}
        """
        return who_liked(obj)


    @library.global_function
    def get_likes_count(obj) -> int:
        """
        Return count of likes for given object

        Usage:
            {{ get_likes_count(object) }}
        """
        return obj_likes_count(obj)

    @library.global_function
    def get_likes(user) -> QuerySet:
        """
        Return likes for current user

        Usage:
            {{ get_likes(request.user) }}
        """
        return Like.objects.filter(sender=user)

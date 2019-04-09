from django.apps import apps


if apps.is_installed('django_jinja'):

    from django.db.models import QuerySet

    from django_jinja import library

    from ..models import Like
    from likes.services import (
        obj_likes_count,
        is_liked,
        get_who_liked as who_liked
    )

    __all__ = (
        'get_likes_count',
        'get_who_liked',
        'get_likes',
        'get_is_liked'
    )

    @library.global_function
    def get_likes_count(obj) -> int:
        """
        Returns count of likes for a given object

        Usage:
            {{ get_likes_count(object) }}
        """
        return obj_likes_count(obj)


    @library.global_function
    def get_who_liked(obj) -> QuerySet:
        """
        Returns users, who liked a given object.

        Usage:
            {{ get_who_liked(object) }}
        """
        return who_liked(obj)

    @library.global_function
    def get_likes(user) -> QuerySet:
        """
        Returns likes for a given user

        Usage:
            {{ get_likes(request.user) }}
        """
        return Like.objects.filter(sender=user)

    @library.global_function
    def get_is_liked(obj, user) -> bool:
        """
        Checks if a given object liked by a given user.

        Usage:
            {{ get_is_liked(object, request.user) }}
        """
        return is_liked(obj, user)

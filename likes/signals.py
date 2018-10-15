import django.dispatch

__all__ = (
    'object_liked',
    'object_unliked'
)


object_liked = django.dispatch.Signal(providing_args=["like", "request"])
object_unliked = django.dispatch.Signal(providing_args=["object", "request"])

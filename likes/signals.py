from django.dispatch import Signal

__all__ = (
    'object_liked',
    'object_unliked'
)


object_liked = Signal(providing_args=["like", "request"])
object_unliked = Signal(providing_args=["object", "request"])

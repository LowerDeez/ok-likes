from django.contrib.contenttypes.models import ContentType
from django.utils.translation import pgettext_lazy

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer

from ..models import Like
from ..utils import get_who_liked

__all__ = (
    'LikedMixin',
)


class LikedMixin:
    """
    Mixin to add two routable actions to ModelViewSets,
    which allows to get "fans" for a current object and "like/unlike" it.
    """
    user_serializer = None  # type: ModelSerializer

    def get_user_serializer(self):
        if not self.user_serializer:
            raise AttributeError(pgettext_lazy('like', '"user_serializer" is not specified.'))
        return self.user_serializer

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def toggle(self, request, pk=None):
        """
        To like/unlike object
        """
        obj = self.get_object()
        ct = ContentType.objects.get_for_model(obj)
        like, created = Like.like(sender=request.user, content_type=ct, object_id=obj.pk)
        return Response({'id': obj.pk, 'content_type': ct.pk, 'is_liked': created})

    @action(detail=True, methods=['GET'])
    def fans(self, request, pk=None):
        """
        Return all users, who liked current object
        """
        obj = self.get_object()
        users = get_who_liked(obj)
        serializer_class = self.get_user_serializer()
        serializer = serializer_class(users, context={'request': request}, many=True)
        return Response(serializer.data)

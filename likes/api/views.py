from rest_framework import status
from rest_framework import filters
from rest_framework.generics import ListAPIView, CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from likes.api.pagination import get_pagination_class
from likes.api.serializers import (
    LikeListSerializer,
    LikeToggleSerializer,
    IsLikedSerializer
)
from likes.models import Like
from likes.services import user_likes_count

__all__ = (
    'UserCountOfLikesAPIView',
    'IsLikedAPIView',
    'LikeListAPIView',
    'LikeToggleView',
)


class UserCountOfLikesAPIView(APIView):
    """
    API View to return count of likes for authenticated user.
    """
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        return Response(
            data={
                'count': user_likes_count(user=request.user)
            }
        )


class IsLikedAPIView(GenericAPIView):
    """
    post:
    API View to check is given elements are liked by authenticated user.\n
    Possible payload:\n
        {
            "type": "app_label.model",  // object's content type's natural key joined string
            "ids": [1,2,3]  // list of objects primary keys
        }
    """
    permission_classes = (AllowAny, )
    serializer_class = IsLikedSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class LikeListAPIView(ListAPIView):
    """
    List API View to return all likes for authenticated user.
    """
    pagination_class = get_pagination_class()
    permission_classes = (IsAuthenticated, )
    serializer_class = LikeListSerializer
    queryset = Like.objects.all()
    filter_backends = (filters.SearchFilter, )
    search_fields = (
        'content_type__model',
    )

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                sender=self.request.user
            )
            .select_related('sender')
            .distinct()
        )


class LikeToggleView(CreateAPIView):
    """
    post:
    API View to like-unlike given object by authenticated user.\n
    Possible payload:\n
        {
            "type": "app_label.model",  // object's content type's natural key joined string
            "id": 1  // object's primary key
        }
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = LikeToggleSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = serializer.data
        data['is_liked'] = getattr(serializer, 'is_liked', True)
        headers = self.get_success_headers(serializer.data)
        return Response(
            data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

from rest_framework import status
from rest_framework import filters
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from likes.api.pagination import get_pagination_class
from likes.api.serializers import (
    LikeSerializer,
    LikeToggleSerializer,
    IsLikedSerializer
)
from likes.models import Like
from likes.services import user_likes_count

__all__ = (
    'LikeListAPIView',
    'LikeToggleView',
    'UserCountOfLikesAPIView',
    'IsLikedAPIView'
)


class LikeListAPIView(ListAPIView):
    """
    List API View to return all likes for authenticated user.
    """
    pagination_class = get_pagination_class()
    permission_classes = (IsAuthenticated, )
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    filter_backends = (filters.SearchFilter, )
    search_fields = ('content_type__model', )

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
            "content_type": 1,  // content type id of object
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
        data['is_liked'] = bool(serializer.instance.pk)
        return Response(
            data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(serializer.data)
        )


class UserCountOfLikesAPIView(APIView):
    """
    API View to return count of likes for authenticated user.
    """
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        return Response(
            data={'count': user_likes_count(request.user)}
        )


class IsLikedAPIView(APIView):
    """
    post:
    API View to check is given elements are liked by authenticated user.\n
    Possible payload:\n
        {
            "content_type": 1,  // content type id of object
            "ids": [1,2,3]  // list of objects primary keys
        }
    """
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        serializer = IsLikedSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(
            data={'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

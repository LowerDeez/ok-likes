from django.urls import include, path
from likes.api.views import (
    LikeListAPIView,
    UserCountOfLikesAPIView,
    LikeToggleView,
    IsLikedAPIView
)

app_name = 'likes-api'

urlpatterns = [
    path('likes/', include([
        path('list/', LikeListAPIView.as_view(), name='list'),
        path('count/', UserCountOfLikesAPIView.as_view(), name='count'),
        path('toggle/', LikeToggleView.as_view(), name='toggle'),
        path('is/', IsLikedAPIView.as_view(), name='is'),
    ]))
]

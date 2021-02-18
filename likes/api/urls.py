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
        path('count/', UserCountOfLikesAPIView.as_view(), name='count'),
        path('is/', IsLikedAPIView.as_view(), name='is'),
        path('list/', LikeListAPIView.as_view(), name='list'),
        path('toggle/', LikeToggleView.as_view(), name='toggle'),
    ]))
]

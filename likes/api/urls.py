from django.urls import include, path
from likes.api.views import (
    LikeListAPIView,
    LikedCountAPIView,
    LikeToggleView,
    LikedIDsAPIView
)

app_name = 'likes-api'

urlpatterns = [
    path('likes/', include([
        path('count/', LikedCountAPIView.as_view(), name='count'),
        path('is/', LikedIDsAPIView.as_view(), name='is'),
        path('toggle/', LikeToggleView.as_view(), name='toggle'),
        path('list/', LikeListAPIView.as_view(), name='list'),
    ]))
]

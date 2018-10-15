from django.urls import include, path
from .views import (
    LikeListAPIView,
    UserCountOfLikesAPIView,
    LikeToggleView,
    IsLikedAPIView
)

app_name = 'like-api'

urlpatterns = [
    path('likes/', include([
        path('', LikeListAPIView.as_view(), name='list-view'),
        path('count/', UserCountOfLikesAPIView.as_view(), name='count-view'),
        path('toggle/', LikeToggleView.as_view(), name='toggle-view'),
        path('is/', IsLikedAPIView.as_view(), name='is-liked-view'),
    ]))
]

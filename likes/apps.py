from django.apps import AppConfig
from django.utils.translation import pgettext_lazy


class LikeConfig(AppConfig):
    name = 'likes'
    verbose_name = pgettext_lazy("ok:likes", "Likes")

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import pgettext_lazy

__all__ = (
    'Like',
)

User = get_user_model()


class Like(models.Model):
    """
    Like model

    Attrs:
        sender (ForeignKey): user, which likes an object
        content_type (ForeignKey): content type of a liked object
        object_id (CharField): primary key of a liked object
        content_object (GenericForeignKey): liked object
        created_at (DateTimeField): when object was created
    """
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="likes",
        verbose_name=pgettext_lazy("ok:likes", "Sender"),
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=pgettext_lazy('ok:likes', 'Content type')
    )
    object_id = models.CharField(
        pgettext_lazy('ok:likes', 'Object id'),
        max_length=50
    )
    content_object = GenericForeignKey(
        'content_type',
        'object_id'
    )
    created_at = models.DateTimeField(
        pgettext_lazy("ok:likes", 'Created at'),
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_at']
        unique_together = (
            (
                "sender",
                "content_type",
                "object_id"
            ),
        )
        verbose_name = pgettext_lazy('ok:likes', 'Like')
        verbose_name_plural = pgettext_lazy('ok:likes', 'Likes')

    def __str__(self) -> str:
        return f"{self.sender} - {self.content_object}"

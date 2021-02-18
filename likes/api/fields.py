from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from likes.settings import LIKES_MODELS

__all__ = (
    'ContentTypeNaturalKeyField',
    'LikedObjectRelatedField',
)


class ContentTypeNaturalKeyField(serializers.CharField):
    default_error_messages = {
        'invalid': _(
            'Must be a valid natural key format: `app_label.model`. '
            'Your value: `{value}`.'
        ),
        'not_exist': _(
            'Content type for natural key `{value}` does not exist.'
        )
    }

    def to_internal_value(self, data):
        try:
            app_label, model = data.split('.')
        except ValueError:
            self.fail('invalid', value=data)

        try:
            ct = ContentType.objects.get_by_natural_key(app_label, model)
        except ContentType.DoesNotExist:
            self.fail('not_exist', value=data)

        return ct


class LikedObjectRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `liked_object` generic relationship.
    """
    def to_representation(self, value):
        for model_path, configuration in LIKES_MODELS.items():
            serializer_path = configuration.get('serializer')

            if not serializer_path:
                return str(value)

            app_label, model_name = model_path.split('.')
            model_class = apps.get_model(app_label, model_name)
            serializer_class = import_string(serializer_path)

            if isinstance(value, model_class):
                return serializer_class(
                    instance=value,
                    context=self.context
                ).data

        return str(value)

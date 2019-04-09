from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.utils.module_loading import import_string
from django.utils.translation import pgettext_lazy

from rest_framework import serializers

from likes.models import Like
from likes.settings import LIKES_MODELS
from likes.utils import allowed_content_type
from likes.services import send_signals

__all__ = (
    'LikedObjectRelatedField',
    'LikeSerializer',
    'LikeToggleSerializer',
    'IsLikedSerializer'
)


class LikedObjectRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `liked_object` generic relationship.
    """

    def to_representation(self, value):
        serializers = {}
        for key, val in LIKES_MODELS.items():
            app_label, model_name = key.split('.')
            serializer_path = val.get('serializer')
            if all([app_label, model_name, serializer_path]):
                serializers[
                    apps.get_model(app_label, model_name)
                ] = import_string(serializer_path)
        for model in serializers.keys():
            if isinstance(value, model):
                return serializers[model](
                    instance=value,
                    context=self.context
                ).data
        return str(value)


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for Like model
    """
    content_object = LikedObjectRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = '__all__'


class LikeToggleSerializer(serializers.ModelSerializer):
    """
    Serializer to like element
    """
    id = serializers.IntegerField(write_only=True)
    content_type = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=ContentType.objects.all())

    class Meta:
        model = Like
        fields = ['id', 'content_type']

    def validate_content_type(self, value):
        if not allowed_content_type(value):
            raise serializers.ValidationError(
                pgettext_lazy('like', 'Not allowed content type')
            )
        return value

    def validate(self, data):
        content_type = data['content_type']
        try:
            obj = content_type.get_object_for_this_type(pk=data['id'])
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                pgettext_lazy('like', 'Object not found.')
            )
        else:
            data['object'] = obj
        return data

    def create(self, validated_data):
        like, created = Like.like(
            self.context['request'].user,
            validated_data['content_type'],
            validated_data['object'].pk
        )
        send_signals(
            created=created,
            request=self.context['request'],
            like=like,
            obj=validated_data['object']
        )
        return like


class IsLikedSerializer(serializers.Serializer):
    """
    Serializer to return liked objects
    """
    ids = serializers.ListField(child=serializers.IntegerField())
    content_type = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=ContentType.objects.all())

    def validate(self, data):
        liked_ids = []
        for id_ in data['ids']:
            is_liked = (
                Like.objects
                .filter(
                    content_type=data['content_type'],
                    object_id=id_,
                    sender=self.context['request'].user
                ).exists()
            )
            if is_liked:
                liked_ids.append(id_)
        data['ids'] = liked_ids
        return data

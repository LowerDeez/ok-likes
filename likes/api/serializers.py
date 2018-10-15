from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.utils.module_loading import import_string
from django.utils.translation import pgettext_lazy

from rest_framework import serializers

from ..models import Like
from ..settings import LIKES_MODELS
from ..signals import object_liked, object_unliked
from ..utils import allowed_content_type

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
        models = {}
        for item in LIKES_MODELS.items():
            app_label, model_name = item[0].split('.')
            serializer_class = item[1].get('serializer')
            if all([app_label, model_name, serializer_class]):
                models[apps.get_model(app_label, model_name)] = import_string(serializer_class)
        for model in models.keys():
            if isinstance(value, model):
                return models[model](value, context=self.context).data
        return value.pk


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
            raise serializers.ValidationError(pgettext_lazy('like', 'Not allowed content type'))
        return value

    def validate(self, data):
        content_type = data['content_type']
        try:
            obj = content_type.get_object_for_this_type(pk=data['id'])
        except ObjectDoesNotExist:
            raise serializers.ValidationError(pgettext_lazy('like', 'Object not found.'))
        else:
            data['object'] = obj
        return data

    def create(self, validated_data):
        like, created = Like.like(
            self.context['request'].user,
            validated_data['content_type'],
            validated_data['object'].pk
        )
        if created:
            object_liked.send(
                sender=Like,
                like=like,
                request=self.context['request']
            )
        else:
            object_unliked.send(
                sender=Like,
                object=validated_data['object'],
                request=self.context['request']
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
        for _id in data['ids']:
            is_liked = (
                Like.objects
                .filter(
                    content_type=data['content_type'],
                    object_id=_id,
                    sender=self.context['request'].user
                ).exists()
            )
            if is_liked:
                liked_ids.append(_id)
        data['ids'] = liked_ids
        return data

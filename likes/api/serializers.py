from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import pgettext_lazy

from rest_framework import serializers

from likes.api.fields import (
    ContentTypeNaturalKeyField,
    LikedObjectRelatedField
)
from likes.models import Like
from likes.utils import allowed_content_type
from likes.services import toggle, send_signals

__all__ = (
    'LikeListSerializer',
    'LikeToggleSerializer',
    'IsLikedSerializer'
)


class LikeListSerializer(serializers.ModelSerializer):
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
    type = ContentTypeNaturalKeyField(write_only=True)

    class Meta:
        model = Like
        fields = [
            'id',
            'type'
        ]

    def validate(self, data):
        content_type = data.pop('type')
        object_id = data.pop('id')

        if not allowed_content_type(content_type):
            raise serializers.ValidationError({
                'type': pgettext_lazy(
                    'ok:likes',
                    'Not allowed content type.'
                )
            })

        try:
            obj = (
                content_type.get_object_for_this_type(
                    pk=object_id
                )
            )
        except ObjectDoesNotExist:
            raise serializers.ValidationError({
                'id': pgettext_lazy(
                    'ok:likes',
                    'Object not found.'
                )
            })
        else:
            data['instance'] = obj

        return data

    def create(self, validated_data):
        instance = validated_data['instance']

        like, created = toggle(
            sender=self.context['request'].user,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.pk
        )

        send_signals(
            created=created,
            request=self.context['request'],
            like=like,
            obj=validated_data['instance']
        )

        return like


class IsLikedSerializer(serializers.Serializer):
    """
    Serializer to return liked objects
    """
    ids = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )
    type = ContentTypeNaturalKeyField(
        write_only=True
    )

    def validate(self, data):
        user = self.context['request'].user

        if not user.is_authenticated:
            ids = []
        else:
            ids = (
                Like.objects
                .filter(
                    content_type=data.pop('type', None),
                    object_id__in=data.pop('ids', []),
                    sender=user
                ).values_list('id', flat=True)
            )

        data['ids'] = list(ids)

        return data

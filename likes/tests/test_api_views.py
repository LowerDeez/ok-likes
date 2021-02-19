import json

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from likes.models import Like
from likes.services import toggle

User = get_user_model()


class BaseAPILikeTestCase(APITestCase):
    def setUp(self):
        self.content_type = ContentType.objects.get(model="user")
        self.username = 'john'
        self.password = 'secret123'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            email='john@doe.com'
        )
        self.test_user = User.objects.create(username='test')
        self.like = toggle(
            user=self.user,
            content_type=self.content_type,
            object_id=self.test_user.pk
        )[0]

    def tearDown(self):
        self.user.delete()
        self.test_user.delete()


class LikeListAPIViewTestCase(BaseAPILikeTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('likes-api:list')

    def test_list(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserCountOfLikesAPIViewTestCase(BaseAPILikeTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('likes-api:count')

    def test_count(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.data.get('count'), 1)


class LikeToggleViewTestCase(BaseAPILikeTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('likes-api:toggle')
        self.valid_payload = {
            'id': self.test_user.pk,
            'type': '.'.join(self.content_type.natural_key()),
        }

    def test_toggle(self):
        self.client.login(username=self.username, password=self.password)

        self.assertEqual(Like.objects.filter(sender=self.user).count(), 1)

        # test unlike
        with self.settings(LIKES_MODELS={'auth.User': {}}):
            self.client.post(
                self.url,
                data=json.dumps(self.valid_payload),
                content_type='application/json'
            )
            self.assertEqual(Like.objects.filter(sender=self.user).count(), 0)

            # test like
            self.client.post(
                self.url,
                data=json.dumps(self.valid_payload),
                content_type='application/json'
            )
            self.assertEqual(Like.objects.filter(sender=self.user).count(), 1)


class IsLikedAPIViewTestCase(BaseAPILikeTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('likes-api:is')
        self.valid_payload = {
            'type': '.'.join(self.content_type.natural_key()),
        }

    def test_is_liked(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(
            self.url,
            data=self.valid_payload,
        )
        self.assertCountEqual(response.data.get('ids'), [str(self.like.content_object.pk)])

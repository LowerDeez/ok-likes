import json

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Like

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
        Like.like(self.user, self.content_type, self.test_user.pk)

    def tearDown(self):
        self.user.delete()
        self.test_user.delete()


class LikeListAPIViewTestCase(BaseAPILikeTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('like-api:list-view')

    def test_list(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserCountOfLikesAPIViewTestCase(BaseAPILikeTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('like-api:count-view')

    def test_count(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.data.get('count'), 1)


class LikeToggleViewTestCase(BaseAPILikeTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('like-api:toggle-view')
        self.valid_payload = {
            'id': self.test_user.pk,
            'content_type': self.content_type.pk,
        }

    def test_toggle(self):
        self.client.login(username=self.username, password=self.password)

        self.assertEqual(Like.objects.filter(sender=self.user).count(), 1)

        # test unlike
        with self.settings(LIKES_MODELS={'auth.User': {}}):
            resp = self.client.post(
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
        self.url = reverse('like-api:is-liked-view')
        self.valid_payload = {
            'ids': [self.test_user.pk],
            'content_type': self.content_type.pk,
        }

    def test_is_liked(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(
            self.url,
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertCountEqual(response.data.get('ids'), [self.test_user.pk])

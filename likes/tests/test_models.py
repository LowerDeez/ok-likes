from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from ..models import Like

User = get_user_model()


class LikeTestCase(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create(username="user 1")
        self.user_2 = User.objects.create(username="user 2")
        self.content_type = ContentType.objects.get(model="user")

    def tearDown(self):
        self.user_1.delete()
        self.user_2.delete()

    def test_str(self):
        like = Like(
            sender=self.user_1,
            content_type=self.content_type,
            object_id=self.user_2.pk
        )
        self.assertEquals(str(like), f"{self.user_1.__str__()} - {self.user_2.__str__()}")

    def test_like(self):
        like, liked = Like.like(self.user_1, self.content_type, self.user_2.pk)
        self.assertTrue(liked)

    def test_unlike(self):
        Like.like(self.user_1, self.content_type, self.user_2.pk)
        like, liked = Like.like(self.user_1, self.content_type, self.user_2.pk)
        self.assertFalse(liked)

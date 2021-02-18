from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from ..models import Like
from ..templatetags.ok_likes import who_liked, likes, likes_count, is_liked

User = get_user_model()


class TemplateTagsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="user")
        self.users = []
        for i in range(6):
            self.users.append(
                User.objects.create(username=str(i))
            )
        Like.objects.create(
            sender=self.user,
            content_type=ContentType.objects.get(model="user"),
            object_id=self.users[0].pk
        )

    def test_likes_count(self):
        self.assertEquals(likes_count(self.users[0]), 1)

    def test_is_liked(self):
        self.assertEquals(is_liked(obj=self.users[0], user=self.user), True)

    def test_likes_all(self):
        qs = likes(self.user)
        self.assertEquals(qs.count(), 1)
        self.assertEquals(qs[0].sender, self.user)
        self.assertEqual(qs[0].content_object, self.users[0])

    def test_who_liked(self):
        fans = list(who_liked(self.users[0]).values_list('id', flat=True))
        self.assertEqual(fans, list(User.objects.filter(pk=self.user.pk).values_list('id', flat=True)))
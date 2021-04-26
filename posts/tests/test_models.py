from django.test import TestCase
from posts.models import Post, User, Group
import datetime


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        test_author = User.objects.create(username='test_user')
        cls.test_group = Group.objects.create(title='test_group',
                                              description='test',
                                              slug='test')
        cls.post = Post.objects.create(
            text='Текст',
            group=cls.test_group,
            author=test_author,
            pub_date=datetime.datetime.today()
        )

    def test_name_title_post(self):
        verbose = Post._meta.get_field('text').verbose_name
        self.assertEqual(verbose, 'текст')

    def test_name_title_group(self):
        verbose = Group._meta.get_field('title').verbose_name
        self.assertEqual(verbose, 'Название')

    def test_post_name(self):
        post = PostModelTest.post
        name = post.text
        self.assertEqual(name, str(post))

    def test_group_name(self):
        group = PostModelTest.test_group
        name = group.title
        self.assertEqual(name, str(group))

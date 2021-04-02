from django.test import TestCase
from posts.models import Post, Group, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        test_author = User.objects.create_user(username='Mark')
        test_group = Group.objects.create(title='test')
        cls.post = Post.objects.create(
            text="test_PostModel",
            pub_date="29.03.2021",
            author=test_author,
            group=test_group,
        )

    def test_text_post(self):
        post = PostModelTest.post
        verbose = post._meta.get_field('text').verbose_name
        self.assertEqual(verbose, 'Текст поста')

    def test_text_help_text(self):
        post = PostModelTest.post
        help_text = post._meta.get_field('text').help_text
        self.assertEqual(help_text, 'Напишите текст поста')

    def test_object_name_is_title_field(self):
        post = PostModelTest.post
        expected_object_name = post.text
        self.assertEqual(expected_object_name, str(post))

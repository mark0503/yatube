from django.test import TestCase, Client
from posts.models import Post, User, Group


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        test_author = User.objects.create_user(username="Mark")
        test_group = Group.objects.create(title="test", slug="test")
        cls.post = Post.objects.create(
            text="test_PostModel",
            pub_date="24.03.2021",
            author=test_author,
            group=test_group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='Mark1')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            'posts/index.html': '/',
            'posts/new.html': '/new/',
            'posts/group.html': '/group/test/',
        }
        for template, reverse_name in templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

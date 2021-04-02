from django.test import TestCase, Client
from posts.models import Post, User, Group
from django.urls import reverse


class PostViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        test_author = User.objects.create_user(username='Mark')
        test_group = Group.objects.create(title='test', slug='test')
        cls.post = Post.objects.create(
            text='test_PostModel',
            pub_date='24.03.2021',
            author=test_author,
            group=test_group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='Mark1')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_use_correct_template(self):
        templates_pages_names = {
            'posts/index.html': reverse('index'),
            'posts/new.html': reverse('new_post'),
            'posts/group.html': (reverse('group', kwargs={'slug': 'test'}))

        }
        for templates, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, templates)

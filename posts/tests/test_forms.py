from django.test import TestCase, Client
from posts.models import Post, User, Group
from django.urls import reverse
from posts.forms import PostForm


class PostFormsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        test_author = User.objects.create_user(username='Mark')
        test_group = Group.objects.create(title='test', slug='test')
        post = Post.objects.create(
            text='test_PostModel',
            pub_date='24.03.2021',
            author=test_author,
            group=test_group,
        )
        cls.form = PostForm()

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='Mark1')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        posts_count = Post.objects.count()
        test_group = Group.objects.get(title='test')
        form_data = {
            "group": test_group.id,
            "text": "Тестовый текст",
        }
        response = self.authorized_client.post(
            reverse("new_post"), data=form_data, follow=True
        )
        self.assertEqual(Post.objects.count() - 1, posts_count)
        self.assertRedirects(response, reverse("index"))
        self.assertTrue(
            Post.objects.filter(group=test_group.id, text="Тестовый текст").exists()
        )
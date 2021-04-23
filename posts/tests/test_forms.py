from django.test import TestCase, Client
from posts.models import Post, Group, User
from django.urls import reverse


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        test_author = User.objects.create(username='test_user')
        test_group = Group.objects.create(title='test_group',
                                          description='test', slug='test')
        cls.post = Post.objects.create(
            text='Текст',
            group=test_group,
            author=test_author,
        )

    def setUp(self):
        self.username = 'test_user1'
        self.user = User.objects.create_user(username=self.username)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.test_group = Group.objects.create(title='test_group3',
                                               description='test3',
                                               slug='test3')
        self.post = Post.objects.create(
            text='Текст',
            group=self.test_group,
            author=self.user,
        )

    def test_create_post(self):
        group = Group.objects.get(title='test_group')
        form_data = {
            "group": group.id,
            "text": 'test',
        }
        response = self.authorized_client.post(
            reverse("new_post"), data=form_data, follow=True
        )
        posts_count = Post.objects.count()
        self.assertRedirects(response, reverse("index"))
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertTrue(
            Post.objects.filter(group=group.id, text='test').exists()
        )

    def test_edit_post(self):
        group = Group.objects.get(title='test_group3')
        posts_count = Post.objects.count()
        form_data = {
            "group": group.id,
            "text": 'test21',
        }
        response = self.authorized_client.post(
            reverse("post_edit",
                    kwargs={'username': self.username,
                            'post_id': self.post.id}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('post_profile',
                                               kwargs={
                                                   'username': self.username,
                                                   'post_id': self.post.id
                                               }))
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertTrue(
            Post.objects.filter(text="test21",
                                group=group.id).exists() 
        )

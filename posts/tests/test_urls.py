from django.test import TestCase, Client
from posts.models import Post, Group, User, Follow
import datetime
from django.urls import reverse


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_homepage(self):
        response = self.guest_client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_author = User.objects.create(username='test_user')
        test_group = Group.objects.create(title='test_group',
                                          description='test', slug='test')
        cls.post = Post.objects.create(
            text='Текст',
            group=test_group,
            author=cls.test_author,
            pub_date=datetime.datetime.today()
        )

    def setUp(self):
        self.guest_client = Client()
        self.username = 'test_user1'
        self.user = User.objects.create_user(username=self.username)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.group = Group.objects.create(title='test_group',
                                          slug='test_group')
        self.user2 = User.objects.create_user(username='mark')
        self.authorized_user = Client()
        self.authorized_user.force_login(self.user2)
        self.guest_client = Client()
        self.post = Post.objects.create(
            text="test_PostModel",
            pub_date="24.03.2021",
            author=self.user,
            group=self.group,
        )

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            reverse('index'): 'index.html',
            reverse('group', args=[self.group]): 'posts/group.html',
            reverse('new_post'): 'posts/new.html',
            reverse('post_edit', kwargs={'username': self.username,
                                         'post_id': self.post.id
                                         }): 'new.html',
        }
        for reverse_name, template in templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_profile(self):
        response = self.guest_client.get(reverse('profile',
                                         kwargs={'username': 'test_user1'}))
        self.assertEqual(response.status_code, 200)

    def test_profile_post(self):
        iid = self.post.id
        response = self.guest_client.get(reverse('post_profile',
                                         kwargs={'username': 'test_user1',
                                                 'post_id': iid}))
        self.assertEqual(response.status_code, 200)

    def test_profile_post_edit(self):
        iid = self.post.id
        response = self.authorized_client.get(
            reverse(
                'post_edit',
                kwargs={
                    'username': 'test_user1',
                    'post_id': iid,
                }
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_profile_post_edit_guest(self):
        response = self.guest_client.get(
            reverse(
                'post_edit',
                kwargs={
                    'username': self.username,
                    'post_id': self.post.id,
                }
            ),
            follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/test_user1/2/edit/'
        )

    def test_profile_post_edit_non_author(self):
        response = self.authorized_user.get(
            reverse(
                'post_edit',
                kwargs={
                    'username': self.username,
                    'post_id': self.post.id,
                }
            ),
            follow=True)
        self.assertRedirects(
            response, reverse(
                'post_profile',
                kwargs={
                    'username': self.username,
                    'post_id': self.post.id,
                }
            )
        )

    def test_404_page(self):
        response = self.guest_client.get('/unknown/page/')
        self.assertEquals(response.status_code, 404)

    def test_profile_follow(self):
        x = 0
        self.authorized_user.get(reverse('profile_follow',
                                 kwargs={'username': 'test_user1'}))
        if Follow.objects.get(user=self.user2, author=self.user):
            x = 1
        self.assertEqual(x, 1)

    def test_profile_unfollow(self):
        x = 0
        self.authorized_user.get(reverse('profile_unfollow',
                                 kwargs={'username': 'test_user'}))
        try:
            Follow.objects.get(user=self.user2, author=self.user)
        except Follow.DoesNotExist:
            x = 1
            pass
        self.assertEqual(x, 1)

    def test_profile_follow(self):
        response = self.authorized_user.get(reverse('profile_follow',
                                            kwargs={'username': 'test_user'}))
        self.assertEqual(response.status_code, 302)

    def test_profile_unfollow(self):
        response = self.authorized_user.get(reverse('profile_unfollow',
                                            kwargs={'username': 'test_user'}))
        self.assertEqual(response.status_code, 302)

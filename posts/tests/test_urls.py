from django.test import TestCase, Client
from posts.models import Post, Group, User
import datetime
from django.urls import reverse 


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_homepage(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)


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
        response = self.guest_client.get('/test_user1/')
        self.assertAlmostEqual(response.status_code, 200)
        response = self.guest_client.get(f'/test_user1/{self.post.id}')
        self.assertAlmostEqual(response.status_code, 301)
        response = self.authorized_client.get(f'/test_user1/{self.post.id}/edit/', follow=True)
        self.assertEqual(response.status_code, 200)
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
            response, f'/{self.username}/{self.post.id}/'
        )
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
            response, f'/{self.username}/{self.post.id}/'
        )

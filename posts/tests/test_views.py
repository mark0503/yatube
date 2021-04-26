import shutil
import tempfile
from django.conf import settings
from django.test import TestCase, Client
from posts.models import Post, Group, User, Follow
from django.urls import reverse
from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache


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
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        User.objects.create(username='test_user')
        cls.test_group = Group.objects.create(title='test_group',
                                              description='test', slug='test')
        cls.author = User.objects.create(username='user_author')
        cls.user = User.objects.create(username='user_user')
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        im = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        cls.post = Post.objects.create(
            text="Текст",
            pub_date="24.03.2021",
            author=cls.author,
            group=cls.test_group,
            image=im,
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        author = TaskURLTests.author
        self.authorized_client.force_login(author)

    def test_pages_use_correct_template(self):
        templates_pages_names = {
            'index.html': reverse('index'),
            'posts/new.html': reverse('new_post'),
            'posts/group.html': (
                reverse('group', kwargs={'slug': 'test'})
            )
        }

        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_home_page_shows_correct_context(self):
        response = self.authorized_client.get(reverse('new_post'))
        form_fields = {
            'text': forms.fields.CharField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_task_list_page_shows_correct_context(self):
        response = self.authorized_client.get(reverse('index'))
        first_object = response.context['page'][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author.username
        post_group_0 = first_object.group.title
        post_image_0 = first_object.image
        self.assertEqual(post_text_0, 'Текст')
        self.assertEqual(post_group_0, 'test_group')
        self.assertEqual(post_author_0, 'user_author')
        self.assertEqual(post_image_0.name, 'posts/small.gif')

    def test_task_detail_pages_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('group', kwargs={'slug': 'test'})
        )
        first_object = response.context['page'][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author.username
        post_group_0 = first_object.group.title
        post_image_0 = first_object.image
        self.assertEqual(post_text_0, 'Текст')
        self.assertEqual(post_group_0, 'test_group')
        self.assertEqual(post_author_0, 'user_author')
        self.assertEqual(post_image_0.name, 'posts/small.gif')

    def test_about_page_accessible_by_name(self):
        response = self.guest_client.get(reverse('about:tech'))
        self.assertEqual(response.status_code, 200)

    def test_about_page_uses_correct_template(self):
        response = self.guest_client.get(reverse('about:author'))
        self.assertTemplateUsed(response, 'about/author.html')

    def test_about_page_accessible_by_name(self):
        response = self.guest_client.get(reverse('about:author'))
        self.assertEqual(response.status_code, 200)

    def test_about_page_uses_correct_template(self):
        response = self.guest_client.get(reverse('about:tech'))
        self.assertTemplateUsed(response, 'about/tech.html')

    def test_home_page_shows_correct_context(self):
        iid = self.post.id
        respons = self.authorized_client.get(reverse('post_edit',
                                             kwargs={'username': 'user_author',
                                                     'post_id': iid}))
        form_fields = {
            'text': forms.fields.CharField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = respons.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_task_in_profile(self):
        response = self.authorized_client.get(
            reverse('post_profile', kwargs={"username": "user_author",
                                            "post_id": self.post.id})
        )
        first_object = response.context['post']
        post_text_0 = first_object.text
        post_author_0 = first_object.author.username
        post_group_0 = first_object.group.title
        post_image_0 = first_object.image
        self.assertEqual(post_text_0, 'Текст')
        self.assertEqual(post_group_0, 'test_group')
        self.assertEqual(post_author_0, 'user_author')
        self.assertEqual(post_image_0.name, 'posts/small.gif')

    def test_post_index_chached(self):
        response_before = self.authorized_client.get(reverse("index"))
        Post.objects.create(
            text='new_text_note',
            author=TaskURLTests.author,
            group=TaskURLTests.test_group,
        )
        response_after = self.authorized_client.get(reverse("index"))
        self.assertEqual(
            response_before.content,
            response_after.content,
        )
        cache.clear()
        after_cache = self.authorized_client.get(reverse("index"))
        self.assertNotEqual(
            response_before.content,
            after_cache.content
        )

    def test_post_follower(self):
        Follow.objects.create(user=TaskURLTests.user,
                              author=TaskURLTests.author)
        Post.objects.create(
            text="test_text",
            author=TaskURLTests.author)
        non_follower = User.objects.create_user(username="test3")
        self.authorized_client.force_login(non_follower)
        response = self.authorized_client.get(reverse("follow_index"))
        self.assertEqual(len(response.context['page']), 0)

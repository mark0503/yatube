from django.test import TestCase, Client
from posts.models import Post, Group, User
from django.urls import reverse
from django import forms


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
        )

    def setUp(self):
        self.user = User.objects.create_user(username='test_user1')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.guest_client = Client()
        self.username = 'test_user2'
        self.user = User.objects.create_user(username=self.username)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.group = Group.objects.create(title='test_group',
                                          slug='test_group')
        self.post = Post.objects.create(
            text="Текст",
            pub_date="24.03.2021",
            author=self.user,
            group=self.group,
        )

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
        self.assertEqual(post_text_0, 'Текст')
        self.assertEqual(post_group_0, 'test_group')
        self.assertEqual(post_author_0, 'test_user2')

    def test_task_detail_pages_show_correct_context(self):
        response = self.authorized_client.get(

            reverse('group', kwargs={'slug': 'test'})
        )
        first_object = response.context['page'][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author.username
        post_group_0 = first_object.group.title
        self.assertEqual(post_text_0, 'Текст')
        self.assertEqual(post_group_0, 'test_group')
        self.assertEqual(post_author_0, 'test_user')

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
        response = self.authorized_client.get(reverse("post_edit",
                                              kwargs={"username": "test_user2",
                                                      "post_id": iid}))
        form_fields = {
            'text': forms.fields.CharField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_task_in_profile(self):
        response = self.authorized_client.get(
                reverse('post_profile', kwargs={"username": "test_user2",
                                                "post_id": self.post.id}
                                                )
                                            )
        first_object = response.context['post']
        post_text_0 = first_object.text
        post_author_0 = first_object.author.username
        post_group_0 = first_object.group.title
        self.assertEqual(post_text_0, 'Текст')
        self.assertEqual(post_group_0, 'test_group')
        self.assertEqual(post_author_0, 'test_user2')

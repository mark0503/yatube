import shutil
import tempfile
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from posts.models import Post, Group, User, Comment
from django.urls import reverse


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        User.objects.create(username='test_user')
        cls.test_group = Group.objects.create(title='test_group',
                                              description='test',
                                              slug='test')
        cls.test_group = Group.objects.create(title='test_group2',
                                              description='test2',
                                              slug='test2')
        cls.username = 'user_author'
        cls.author = User.objects.create(username=cls.username)
        cls.user = User.objects.create(username='user_user')
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif',
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
        self.post = Post.objects.create(
            text='Текст',
            group=TaskURLTests.test_group,
            author=TaskURLTests.author,
        )

    def test_create_post(self):
        group = Group.objects.get(title='test_group')
        form_data = {
            "group": group.id,
            "text": 'test',
            "image": TaskURLTests.uploaded
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
        group = Group.objects.get(title='test_group2')
        posts_count = Post.objects.count()
        form_data = {
            "group": group.id,
            "text": 'test21',
        }
        response = self.authorized_client.post(
            reverse("post_edit",
                    kwargs={'username': TaskURLTests.username,
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

    def test_comment_guest(self):
        comment_count = Comment.objects.count()
        form_data = {
            'text': 'test_comm',
        }
        self.guest_client.post(
            reverse("add_comment",
                    kwargs={'username': TaskURLTests.username,
                            'post_id': self.post.id}),
            data=form_data,
            follow=True
        )
        coment_count_later = Comment.objects.count()
        self.assertEqual(comment_count, coment_count_later)

    def test_comment_author(self):
        comment_count = Comment.objects.count()
        form_data = {
            'text': 'test_comm',
        }
        self.authorized_client.post(
            reverse("add_comment",
                    kwargs={'username': TaskURLTests.username,
                            'post_id': self.post.id}),
            data=form_data,
            follow=True
        )
        coment_count_later = Comment.objects.count()
        self.assertNotEqual(comment_count, coment_count_later)

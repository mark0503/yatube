from posts.models import Post, Group, User
from django.urls import reverse
from django.test import TestCase


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        test_author = User.objects.create(username='test_user')
        test_group = Group.objects.create(title='test_group',
                                          description='test',
                                          slug='test')
        cls.post = Post.objects.create(
            text='Текст1',
            group=test_group,
            author=test_author,
        ),
        Post.objects.create(
            text='Текст2',
            group=test_group,
            author=test_author,
        ),
        Post.objects.create(
            text='Текст3',
            group=test_group,
            author=test_author,
        ),
        Post.objects.create(
            text='Текст4',
            group=test_group,
            author=test_author,
        ),
        Post.objects.create(
            text='Текст5',
            group=test_group,
            author=test_author,
        ),
        Post.objects.create(
            text='Текст6',
            group=test_group,
            author=test_author,
        ),
        Post.objects.create(
            text='Текст7',
            group=test_group,
            author=test_author,
        ),
        Post.objects.create(
            text='Текст8',
            group=test_group,
            author=test_author,
        ),
        Post.objects.create(
            text='Текст9',
            group=test_group,
            author=test_author,
        ),
        Post.objects.create(
            text='Текст10',
            group=test_group,
            author=test_author,
        ),
        Post.objects.create(
            text='Текст11',
            group=test_group,
            author=test_author,
        ),
        Post.objects.create(
            text='Текст12',
            group=test_group,
            author=test_author,
        ),
        Post.objects.create(
            text='Текст13',
            group=test_group,
            author=test_author,
        )

    def test_first_page_contains_ten_records(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(len(response.context.get('page').object_list), 10)

    def test_second_page_contains_three_records(self):
        response = self.client.get(reverse('index') + '?page=2')
        self.assertEqual(len(response.context.get('page').object_list), 3)

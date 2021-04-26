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
        cls.obj = (Post(text='Тестовый текст %s' % i,
                        author=test_author,
                        group=test_group) for i in range(13))
        cls.test_posts = Post.objects.bulk_create(cls.obj)

    def test_first_page_contains_ten_records(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(len(response.context.get('page').object_list), 10)

    def test_second_page_contains_three_records(self):
        response = self.client.get(reverse('index') + '?page=2')
        self.assertEqual(len(response.context.get('page').object_list), 3)

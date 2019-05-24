import uuid
from django.test import TestCase
from download.models import PostModel


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        PostModel.objects.create(post_url="https://www.instagram.com/p/Bx0qIjAgiv7")

    def setUp(self):
        self.url = "https://www.instagram.com/p/Bx0qIjAgiv7"

    def test_object_name(self):
        post = PostModel.objects.get(post_url=self.url)
        expected_name = f"URL: {self.url}"
        self.assertEqual(str(post), expected_name)

    def test_post_url_label(self):
        post = PostModel.objects.get(post_url=self.url)
        field_label = post._meta.get_field('post_url').verbose_name
        self.assertEqual(field_label, 'post url')

    def test_date_time_label(self):
        post = PostModel.objects.get(post_url=self.url)
        field_label = post._meta.get_field('date_time').verbose_name
        self.assertEqual(field_label, 'date time')

    def test_date_time_auto_no_is_true(self):
        post = PostModel.objects.get(post_url=self.url)
        field_option = post._meta.get_field('date_time').auto_now
        self.assertTrue(field_option)

    def test_id_label(self):
        post = PostModel.objects.get(post_url=self.url)
        field_label = post._meta.get_field('id').verbose_name
        self.assertEqual(field_label, 'id')

    def test_id_is_primary_key(self):
        post = PostModel.objects.get(post_url=self.url)
        field_option = post._meta.get_field('id').primary_key
        self.assertTrue(field_option)

    def test_default_id_is_uuid(self):
        post = PostModel.objects.get(post_url=self.url)
        field_option = post._meta.get_field('id').default
        self.assertEqual(type(field_option), type(uuid.uuid4))

    def test_id_is_not_editable(self):
        post = PostModel.objects.get(post_url=self.url)
        field_option = post._meta.get_field('id').editable
        self.assertFalse(field_option)

from django.test import TestCase
from django.urls import reverse
from django.test import Client
from shastra_compedium.tests.factories import (
    CategoryFactory,
    SourceFactory,
    UserFactory,
)
from shastra_compedium.site_text import user_messages
from shastra_compedium.tests.functions import login_as
from shastra_compedium.models import CategoryDetail


class TestUploadChapter(TestCase):
    '''Tests for source create & update'''

    add_name = 'chapter-add'

    def setUp(self):
        self.client = Client()
        self.create_url = reverse(self.add_name,
                                  urlconf='shastra_compedium.urls')
        user = UserFactory()
        login_as(user, self)

    def chapter_data(self):
        self.category = CategoryFactory()
        self.source = SourceFactory()
        return {'sources': [self.source.pk],
                'category': self.category.pk,
                'usage': "test",
                'chapter': 1,
                'contents': "Contents",
                'position_text': "Position text",
                'verse_start': 10,
                'verse_end': 20,
                'step': 0,
                'next': True}

    def test_create_get(self):
        response = self.client.get(self.create_url, follow=True)
        self.assertContains(response, "Upload Chapter")
        self.assertContains(
            response,
            user_messages['CHAPTER_BASICS_INTRO']['description'])
        self.assertContains(response, "Sources")

    def test_create_post_basics_success(self):
        start = CategoryDetail.objects.all().count()
        response = self.client.post(self.create_url,
                                    data=self.chapter_data(),
                                    follow=True)
        self.assertEqual(start + 1, CategoryDetail.objects.all().count())
        self.assertContains(
            response,
            user_messages['CHAPTER_DETAIL_INTRO']['description'])

    def test_create_error(self):
        data = self.chapter_data()
        data['category'] = self.category.pk + 1
        response = self.client.post(self.create_url, data=data, follow=True)
        self.assertNotContains(
            response,
            "Upload Chapter - Edit Detail Entries")
        self.assertContains(
            response,
            "Select a valid choice. That choice is not one of the " +
            "available choices.")
        self.assertContains(
            response,
            user_messages['CHAPTER_BASICS_INTRO']['description'])

from django.test import TestCase
from django.urls import reverse
from django.test import Client
from shastra_compedium.tests.factories import (
    ShastraFactory,
    SourceFactory,
    UserFactory,
)
from shastra_compedium.site_text import make_source_messages
from shastra_compedium.tests.functions import login_as
from shastra_compedium.models import Source


class TestMakeSource(TestCase):
    '''Tests for source create & update'''

    add_name = 'source-add'
    update_name = 'source-update'

    def setUp(self):
        self.client = Client()
        self.object = SourceFactory()
        self.create_url = reverse(self.add_name,
                                  urlconf='shastra_compedium.urls')
        self.edit_url = reverse(self.update_name,
                                args=[self.object.pk],
                                urlconf='shastra_compedium.urls')
        user = UserFactory()
        login_as(user, self)

    def source_data(self):
        return {'title': "New Title",
                'shastra': ShastraFactory().pk,
                'translation_language': "English",
                'translator': "Ted Translator",
                'isbn': "111-222222233333333-0",
                'bibliography': "Tile, Author, Publisher, the like",
                'url': "https://www.books.com/urlforbook"}

    def test_create_get(self):
        response = self.client.get(self.create_url, follow=True)
        self.assertContains(response, "Create Source")
        self.assertContains(response, make_source_messages['create_intro'])
        self.assertContains(response, "Title")

    def test_create_post(self):
        start = Source.objects.all().count()
        response = self.client.post(self.create_url,
                                    data=self.source_data(),
                                    follow=True)
        self.assertContains(
            response,
            make_source_messages['create_success'] % "New Title")
        self.assertEqual(start + 1, Source.objects.all().count())

    def test_create_error(self):
        data = self.source_data()
        data['url'] = "bad url"
        response = self.client.post(self.create_url, data=data, follow=True)
        self.assertNotContains(
            response,
            make_source_messages['create_success'] % "New Title")
        self.assertContains(response, "Enter a valid URL.")
        self.assertContains(response, make_source_messages['create_intro'])

    def test_edit_get(self):
        response = self.client.get(self.edit_url)
        self.assertContains(response, "Update Source")
        self.assertContains(response, make_source_messages['edit_intro'])
        self.assertContains(response, "Title")

    def test_edit_post(self):
        start = Source.objects.all().count()
        response = self.client.post(self.edit_url,
                                    data=self.source_data(),
                                    follow=True)
        self.assertContains(
            response,
            make_source_messages['edit_success'] % "New Title")
        self.assertEqual(start, Source.objects.all().count())

    def test_edit_bad_data(self):
        data = self.source_data()
        data['url'] = "bad url"
        response = self.client.post(self.edit_url, data=data, follow=True)
        self.assertNotContains(
            response,
            make_source_messages['edit_success'] % "New Title")
        self.assertContains(response, "Enter a valid URL.")
        self.assertContains(response, make_source_messages['edit_intro'])

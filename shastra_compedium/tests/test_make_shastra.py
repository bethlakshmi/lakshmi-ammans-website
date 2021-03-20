from django.test import TestCase
from django.urls import reverse
from django.test import Client
from shastra_compedium.tests.factories import (
    ShastraFactory,
    UserFactory,
)
from shastra_compedium.site_text import make_shastra_messages
from shastra_compedium.tests.functions import login_as
from shastra_compedium.models import Shastra


class TestMakeShastra(TestCase):
    '''Tests for shastra create & update'''

    add_name = 'shastra-add'
    update_name = 'shastra-update'

    def setUp(self):
        self.client = Client()
        self.object = ShastraFactory()
        self.create_url = reverse(self.add_name,
                                  urlconf='shastra_compedium.urls')
        self.edit_url = reverse(self.update_name,
                                args=[self.object.pk],
                                urlconf='shastra_compedium.urls')
        user = UserFactory()
        login_as(user, self)

    def shastra_data(self):
        return {'title': "New Title",
                'author': "Author",
                'language': "Sanskrit",
                'min_age': 0,
                'max_age': 100,
                'description': "Description"}

    def test_create_get(self):
        response = self.client.get(self.create_url, follow=True)
        self.assertContains(response, "Create Shastra")
        self.assertContains(response, make_shastra_messages['create_intro'])
        self.assertContains(response, "Title")

    def test_create_post(self):
        start = Shastra.objects.all().count()
        response = self.client.post(self.create_url,
                                    data=self.shastra_data(),
                                    follow=True)
        self.assertContains(
            response,
            make_shastra_messages['create_success'] % "New Title")
        self.assertEqual(start + 1, Shastra.objects.all().count())

    def test_create_error(self):
        data = self.shastra_data()
        data['min_age'] = "bad"
        response = self.client.post(self.create_url, data=data, follow=True)
        self.assertNotContains(
            response,
            make_shastra_messages['create_success'] % "New Title")
        self.assertContains(response, "Enter a whole number.")
        self.assertContains(response, make_shastra_messages['create_intro'])

    def test_get_edit_shastra(self):
        response = self.client.get(self.edit_url)
        self.assertContains(response, "Update Shastra")
        self.assertContains(response, make_shastra_messages['edit_intro'])
        self.assertContains(response, "Title")

    def test_edit_shastra_post(self):
        start = Shastra.objects.all().count()
        response = self.client.post(self.edit_url,
                                    data=self.shastra_data(),
                                    follow=True)
        self.assertContains(
            response,
            make_shastra_messages['edit_success'] % "New Title")
        self.assertEqual(start, Shastra.objects.all().count())

    def test_edit_shastra_bad_data(self):
        data = self.shastra_data()
        data['min_age'] = "bad"
        response = self.client.post(self.edit_url, data=data, follow=True)
        self.assertNotContains(
            response,
            make_shastra_messages['edit_success'] % "New Title")
        self.assertContains(response, "Enter a whole number.")
        self.assertContains(response, make_shastra_messages['edit_intro'])

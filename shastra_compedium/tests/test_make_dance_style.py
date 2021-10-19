from django.test import TestCase
from django.urls import reverse
from django.test import Client
from shastra_compedium.tests.factories import (
    DanceStyleFactory,
    UserFactory,
)
from shastra_compedium.site_text import make_dance_style_messages
from shastra_compedium.tests.functions import login_as
from shastra_compedium.models import DanceStyle


class TestMakeDanceStyle(TestCase):
    '''Tests for Dance Style create & update'''

    add_name = 'dancestyle-add'
    update_name = 'dancestyle-update'

    def setUp(self):
        self.client = Client()
        self.object = DanceStyleFactory()
        self.create_url = reverse(self.add_name,
                                  urlconf='shastra_compedium.urls')
        self.edit_url = reverse(self.update_name,
                                args=[self.object.pk],
                                urlconf='shastra_compedium.urls')
        user = UserFactory()
        login_as(user, self)

    def dance_style_data(self):
        return {'name': "New Style",
                'description': "Description"}

    def test_create_get(self):
        response = self.client.get(self.create_url, follow=True)
        self.assertContains(response, "Create Dance Style")
        self.assertContains(response, make_dance_style_messages['create_intro'])
        self.assertContains(response, "Style")

    def test_create_post(self):
        start = DanceStyle.objects.all().count()
        response = self.client.post(self.create_url,
                                    data=self.dance_style_data(),
                                    follow=True)
        self.assertContains(
            response,
            make_dance_style_messages['create_success'] % "New Style")
        self.assertEqual(start + 1, DanceStyle.objects.all().count())

    def test_create_error(self):
        data = self.dance_style_data()
        del data['description']
        response = self.client.post(self.create_url, data=data, follow=True)
        self.assertNotContains(
            response,
            make_dance_style_messages['create_success'] % "New Style")
        self.assertContains(response, "This field is required.")
        self.assertContains(response, make_dance_style_messages['create_intro'])

    def test_get_edit(self):
        response = self.client.get(self.edit_url)
        self.assertContains(response, "Update Dance Style")
        self.assertContains(response, make_dance_style_messages['edit_intro'])
        self.assertContains(response, "Style")

    def test_post_edit(self):
        start = DanceStyle.objects.all().count()
        response = self.client.post(self.edit_url,
                                    data=self.dance_style_data(),
                                    follow=True)
        self.assertContains(
            response,
            make_dance_style_messages['edit_success'] % "New Style")
        self.assertEqual(start, DanceStyle.objects.all().count())

    def test_edit_bad_data(self):
        data = self.dance_style_data()
        del data['description']
        response = self.client.post(self.edit_url, data=data, follow=True)
        self.assertNotContains(
            response,
            make_dance_style_messages['edit_success'] % "New Style")
        self.assertContains(response, "This field is required.")
        self.assertContains(response, make_dance_style_messages['edit_intro'])

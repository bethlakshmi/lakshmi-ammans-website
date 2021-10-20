from django.test import TestCase
from django.urls import reverse
from django.test import Client
from shastra_compedium.tests.factories import (
    PerformerFactory,
    UserFactory,
)
from shastra_compedium.tests.functions import login_as


class TestCMSMenus(TestCase):
    '''Tests for Account Menu logic'''

    add_name = 'performer-add'
    update_name = 'performer-update'

    def setUp(self):
        self.client = Client()
        self.object = PerformerFactory()
        self.create_url = reverse(self.add_name,
                                  urlconf='shastra_compedium.urls')
        self.edit_url = reverse(self.update_name,
                                args=[self.object.pk],
                                urlconf='shastra_compedium.urls')

    def test_logged_in_no_performer(self):
        self.user = UserFactory()
        login_as(self.user, self)
        response = self.client.get(self.create_url, follow=True)
        self.assertContains(response, self.create_url)
        self.assertNotContains(response, "/performer/update/")

    def test_logged_in_with_performer(self):
        self.user = self.object.contact
        login_as(self.user, self)
        response = self.client.get(self.create_url)
        self.assertNotContains(response, self.create_url)
        self.assertContains(response, self.edit_url)

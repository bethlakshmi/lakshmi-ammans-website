from django.test import TestCase
from django.urls import reverse
from django.test import Client
from shastra_compedium.tests.factories import (
    DanceStyleFactory,
    PerformerFactory,
    UserFactory,
)
from shastra_compedium.tests.functions import login_as
from shastra_compedium.models import Performer


class TestViewDanceStyle(TestCase):
    '''Tests for Performer create & update'''

    view_name = 'dancestyle-view'
    update_name = 'dancestyle-update'
    options = {'size': (350, 350), 'crop': False}

    def setUp(self):
        self.client = Client()
        self.object = DanceStyleFactory()
        self.performer = PerformerFactory(dance_styles=[self.object])
        self.view_url = reverse(self.view_name,
                                args=[self.object.pk],
                                urlconf='shastra_compedium.urls')
        self.edit_url = reverse(self.update_name,
                                args=[self.object.pk],
                                urlconf='shastra_compedium.urls')
        self.user = UserFactory()

    def test_view_w_login(self):
        login_as(self.user, self)
        response = self.client.get(self.view_url)
        self.assertContains(response, self.object.name)
        self.assertContains(response, self.object.description)
        self.assertContains(response, self.performer.name)
        self.assertContains(response, self.edit_url)
        self.assertContains(response, reverse(
            "performer-view",
            args=[self.performer.pk],
            urlconf='shastra_compedium.urls'))

    def test_view_no_login(self):
        response = self.client.get(self.view_url)
        self.assertContains(response, self.object.name)
        self.assertNotContains(response, self.edit_url)

    def test_edit_wrong_style(self):
        response = self.client.get(reverse(self.view_name,
                                args=[self.object.pk+100],
                                urlconf='shastra_compedium.urls'))
        self.assertEqual(404, response.status_code)

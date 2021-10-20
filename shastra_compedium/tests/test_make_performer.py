from django.test import TestCase
from django.urls import reverse
from django.test import Client
from shastra_compedium.tests.factories import (
    DanceStyleFactory,
    PerformerFactory,
    UserFactory,
)
from shastra_compedium.site_text import make_performer_messages
from shastra_compedium.tests.functions import (
    login_as,
    set_image,
)
from shastra_compedium.models import Performer


class TestMakePerformer(TestCase):
    '''Tests for Performer create & update'''

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

    def performer_data(self):
        current_img = set_image(folder_name="performers")
        return {'name': "New Performer",
                'linneage': "linneage text",
                'dance_styles': [DanceStyleFactory().pk],
                'bio': "Perf Bio",
                'contact': self.user.pk,
                'image': current_img.pk}

    def test_create_get(self):
        self.user = UserFactory()
        login_as(self.user, self)
        response = self.client.get(self.create_url, follow=True)
        self.assertContains(response, "Create Performer")
        self.assertContains(response, make_performer_messages['create_intro'])
        self.assertContains(response, "Performer")

    def test_create_post(self):
        self.user = UserFactory()
        login_as(self.user, self)
        start = Performer.objects.all().count()
        response = self.client.post(self.create_url,
                                    data=self.performer_data(),
                                    follow=True)
        self.assertContains(
            response,
            make_performer_messages['create_success'] % "New Performer")
        self.assertEqual(start + 1, Performer.objects.all().count())

    def test_create_error(self):
        self.user = UserFactory()
        login_as(self.user, self)
        data = self.performer_data()
        del data['linneage']
        response = self.client.post(self.create_url, data=data, follow=True)
        self.assertNotContains(
            response,
            make_performer_messages['create_success'] % "New Performer")
        self.assertContains(response, "This field is required.")
        self.assertContains(response, make_performer_messages['create_intro'])

    def test_get_edit(self):
        self.user = self.object.contact
        login_as(self.user, self)
        response = self.client.get(self.edit_url)
        self.assertContains(response, "Update Performer")
        self.assertContains(response, make_performer_messages['edit_intro'])
        self.assertContains(response, "Style")

    def test_post_edit(self):
        self.user = self.object.contact
        login_as(self.user, self)
        start = Performer.objects.all().count()
        response = self.client.post(self.edit_url,
                                    data=self.performer_data(),
                                    follow=True)
        self.assertContains(
            response,
            make_performer_messages['edit_success'] % "New Performer")
        self.assertEqual(start, Performer.objects.all().count())

    def test_edit_bad_data(self):
        self.user = self.object.contact
        login_as(self.user, self)
        data = self.performer_data()
        del data['linneage']
        response = self.client.post(self.edit_url, data=data, follow=True)
        self.assertNotContains(
            response,
            make_performer_messages['edit_success'] % "New Performer")
        self.assertContains(response, "This field is required.")
        self.assertContains(response, make_performer_messages['edit_intro'])

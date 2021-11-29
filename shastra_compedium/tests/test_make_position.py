from django.test import TestCase
from django.urls import reverse
from django.test import Client
from shastra_compedium.tests.factories import (
    CategoryFactory,
    PositionFactory,
    UserFactory,
)
from shastra_compedium.site_text import make_position_messages
from shastra_compedium.tests.functions import login_as
from shastra_compedium.models import Position


class TestMakePosition(TestCase):
    '''Tests for position create & update'''

    add_name = 'position-add'
    update_name = 'position-update'

    def setUp(self):
        self.client = Client()
        self.object = PositionFactory()
        self.create_url = reverse(self.add_name,
                                  urlconf='shastra_compedium.urls')
        self.edit_url = reverse(self.update_name,
                                args=[self.object.pk],
                                urlconf='shastra_compedium.urls')
        user = UserFactory()
        login_as(user, self)

    def position_data(self):
        self.category = CategoryFactory()
        return {'name': "New Name",
                'category': self.category.pk,
                'order': 0}

    def test_create_get(self):
        response = self.client.get(self.create_url, follow=True)
        self.assertContains(response, "Create Position")
        self.assertContains(response, make_position_messages['create_intro'])
        self.assertContains(response, "Name")

    def test_create_get_pre_filled_url(self):
        category = CategoryFactory()
        response = self.client.get(
            reverse(self.add_name,
                    urlconf='shastra_compedium.urls',
                    args=[1, category.pk]),
            follow=True)
        self.assertContains(response, "Create Position")
        self.assertContains(
            response,
            '<option value="%d" selected>%s</option>' % (
                category.pk,
                category.name),
            html=True)
        self.assertContains(
            response,
            '<input type="number" name="order" value="1" required ' +
            'id="id_order">',
            html=True)

    def test_create_post(self):
        start = Position.objects.all().count()
        response = self.client.post(self.create_url,
                                    data=self.position_data(),
                                    follow=True)
        self.assertContains(
            response,
            make_position_messages['create_success'] % "New Name")
        self.assertEqual(start + 1, Position.objects.all().count())

    def test_create_error(self):
        data = self.position_data()
        data['name'] = ""
        response = self.client.post(self.create_url, data=data, follow=True)
        self.assertNotContains(
            response,
            make_position_messages['create_success'] % "New Name")
        self.assertContains(response, "This field is required.")
        self.assertContains(response, make_position_messages['create_intro'])

    def test_edit_get(self):
        response = self.client.get(self.edit_url)
        self.assertContains(response, "Update Position")
        self.assertContains(response, make_position_messages['edit_intro'])
        self.assertContains(response, "Name")

    def test_edit_post(self):
        start = Position.objects.all().count()
        response = self.client.post(self.edit_url,
                                    data=self.position_data(),
                                    follow=True)
        self.assertContains(
            response,
            make_position_messages['edit_success'] % "%s, %s" % (
                "New Name", self.category.name))
        self.assertEqual(start, Position.objects.all().count())

    def test_edit_bad_data(self):
        data = self.position_data()
        data['name'] = ""
        response = self.client.post(self.edit_url, data=data, follow=True)
        self.assertNotContains(
            response,
            make_position_messages['edit_success'] % "New Name")
        self.assertContains(response, "This field is required.")
        self.assertContains(response, make_position_messages['edit_intro'])

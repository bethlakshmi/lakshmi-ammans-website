from django.test import TestCase
from django.test import Client
from django.urls import reverse
from shastra_compedium.tests.factories import (
    CategoryFactory,
    PositionDetailFactory,
    PositionFactory,
    SourceFactory,
    UserFactory,
)
from shastra_compedium.tests.functions import login_as
import json


class TestPositionDetailAutoComplete(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.detail = PositionDetailFactory()
        self.detail2 = PositionDetailFactory()

    def test_list_positiondetail(self):
        login_as(self.user, self)
        response = self.client.get(reverse('positiondetail-autocomplete'))
        self.assertContains(response, str(self.detail))
        self.assertContains(response, self.detail.pk)

    def test_no_access_positiondetails(self):
        response = self.client.get(reverse('positiondetail-autocomplete'))
        self.assertNotContains(response, str(self.detail))
        self.assertNotContains(response, self.detail.pk)

    def test_list_positiondetails_w_search_critieria(self):
        login_as(self.user, self)
        response = self.client.get("%s?q=%s" % (
            reverse('positiondetail-autocomplete'),
            self.detail.position.name))
        self.assertContains(response, str(self.detail))
        self.assertContains(response, self.detail.pk)
        self.assertNotContains(response, str(self.detail2))

    def test_list_positiondetail_w_usage(self):
        login_as(self.user, self)
        response = self.client.get("%s?forward=%s" % (
            reverse('positiondetail-autocomplete'),
            json.dumps({'usage': self.detail.usage, })))
        print(response.content)
        self.assertContains(response, str(self.detail))
        self.assertNotContains(response, str(self.detail2))

    def test_list_positiondetail_w_id(self):
        login_as(self.user, self)
        response = self.client.get("%s?forward=%s" % (
            reverse('positiondetail-autocomplete'),
            json.dumps({'id': self.detail2.id, })))
        self.assertContains(response, str(self.detail))
        self.assertNotContains(response, str(self.detail2))

    def test_list_positiondetail_w_position(self):
        login_as(self.user, self)
        response = self.client.get("%s?forward=%s" % (
            reverse('positiondetail-autocomplete'),
            json.dumps({"position_only": self.detail.position.id, })))
        self.assertContains(response, str(self.detail))
        self.assertNotContains(response, str(self.detail2))

    def test_list_positiondetail_w_position_exclusion(self):
        login_as(self.user, self)
        response = self.client.get("%s?forward=%s" % (
            reverse('positiondetail-autocomplete'),
            json.dumps({"position": self.detail2.position.id, })))
        self.assertContains(response, str(self.detail))
        self.assertNotContains(response, str(self.detail2))

    def test_list_positiondetail_w_sources(self):
        source = SourceFactory()
        self.detail.sources.add(source)
        login_as(self.user, self)
        response = self.client.get("%s?forward=%s" % (
            reverse('positiondetail-autocomplete'),
            json.dumps({"sources": [source.pk], })))
        self.assertContains(response, str(self.detail))
        self.assertNotContains(response, str(self.detail2))

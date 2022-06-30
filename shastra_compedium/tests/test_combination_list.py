from django.test import TestCase
from django.test import Client
from django.urls import reverse
from shastra_compedium.tests.factories import (
    CombinationDetailFactory,
    SourceFactory,
    UserFactory
)
from shastra_compedium.models import CombinationDetail
from shastra_compedium.tests.functions import (
    login_as,
    set_image
)
from filer.models.imagemodels import Image


class TestImageList(TestCase):
    view_name = "combo_list"

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.combo = CombinationDetailFactory()
        self.combo.sources.add(SourceFactory())
        self.url = reverse(self.view_name, urlconf="shastra_compedium.urls")

    def test_list_basic_no_login(self):
        response = self.client.get(self.url)
        self.assertContains(response, self.combo.positions.first().name)
        self.assertContains(response, self.combo.usage)
        self.assertContains(response, self.combo.sources.first().title)
        self.assertContains(response, self.combo.contents)
        self.assertContains(response, reverse(
            "position-view",
            args=[self.combo.positions.first().pk],
            urlconf="shastra_compedium.urls"))
        self.assertNotContains(response, reverse(
            "combination-update",
            args=[self.combo.pk],
            urlconf="shastra_compedium.urls"))

    def test_list_w_login(self):
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, self.combo.contents)
        self.assertContains(response, reverse(
            "position-view",
            args=[self.combo.positions.first().pk],
            urlconf="shastra_compedium.urls"))
        self.assertContains(response, reverse(
            "combination-update",
            args=[self.combo.pk],
            urlconf="shastra_compedium.urls"))

    def test_list_empty(self):
        contents = self.combo.contents
        CombinationDetail.objects.all().delete()
        response = self.client.get(self.url)
        self.assertNotContains(response, contents)

from django.test import TestCase
from django.test import Client
from django.urls import reverse
from shastra_compedium.tests.factories import (
    CategoryFactory,
    PositionFactory,
    UserFactory,
)
from shastra_compedium.tests.functions import login_as


class TestAutoComplete(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()

    def test_list_positions(self):
        position = PositionFactory()
        login_as(self.user, self)
        response = self.client.get(reverse('position-autocomplete'))
        self.assertContains(response, position.name)
        self.assertContains(response, position.pk)

    def test_no_access_positions(self):
        position = PositionFactory()
        response = self.client.get(reverse('position-autocomplete'))
        self.assertNotContains(response, position.name)
        self.assertNotContains(response, position.pk)

    def test_list_positions_w_search_critieria(self):
        position = PositionFactory()
        position2 = PositionFactory()
        login_as(self.user, self)
        response = self.client.get("%s?q=%s" % (
            reverse('position-autocomplete'),
            position.name))
        self.assertContains(response, position.name)
        self.assertContains(response, position.pk)
        self.assertNotContains(response, position2.name)

    def test_list_categories(self):
        category = CategoryFactory()
        login_as(self.user, self)
        response = self.client.get(reverse('category-autocomplete'))
        self.assertContains(response, category.name)
        self.assertContains(response, category.pk)

    def test_no_access_categories(self):
        category = CategoryFactory()
        response = self.client.get(reverse('category-autocomplete'))
        self.assertNotContains(response, category.name)
        self.assertNotContains(response, category.pk)

    def test_list_categories_w_search_critieria(self):
        category = CategoryFactory()
        category2 = CategoryFactory()
        login_as(self.user, self)
        response = self.client.get("%s?q=%s" % (
            reverse('category-autocomplete'),
            category.name))
        self.assertContains(response, category.name)
        self.assertContains(response, category.pk)
        self.assertNotContains(response, category2.name)

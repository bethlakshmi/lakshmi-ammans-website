from django.test import TestCase
from django.test import Client
from django.urls import reverse
from shastra_compedium.tests.factories import (
    CategoryFactory,
    CombinationDetailFactory,
    PositionFactory,
    SourceFactory,
    SubjectFactory,
    UserFactory,
)
from shastra_compedium.tests.functions import login_as
from django.utils.html import strip_tags
import json


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

    def test_list_positions_w_search_criteria(self):
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

    def test_list_combinations(self):
        obj = CombinationDetailFactory()
        obj.sources.add(SourceFactory())
        login_as(self.user, self)
        response = self.client.get(reverse('combination-autocomplete'))
        self.assertContains(response, strip_tags(obj.contents)[0:25])
        self.assertContains(response, obj.pk)

    def test_no_access_combinations(self):
        obj = CombinationDetailFactory()
        obj.sources.add(SourceFactory())
        response = self.client.get(reverse('combination-autocomplete'))
        self.assertNotContains(response, strip_tags(obj.contents)[0:25])
        self.assertNotContains(response, obj.pk)

    def test_list_combinations_w_search_critieria(self):
        obj = CombinationDetailFactory(contents="special stuff")
        obj2 = CombinationDetailFactory()
        obj.sources.add(SourceFactory())
        obj2.sources.add(SourceFactory())
        login_as(self.user, self)
        response = self.client.get("%s?q=%s" % (
            reverse('combination-autocomplete'),
            "special"))
        self.assertContains(response, strip_tags(obj.contents)[0:25])
        self.assertContains(response, obj.pk)
        self.assertNotContains(response, strip_tags(obj2.contents)[0:25])

    def test_list_combination_w_subject(self):
        obj = CombinationDetailFactory(contents="special stuff")
        obj2 = CombinationDetailFactory()
        obj.sources.add(SourceFactory())
        obj2.sources.add(SourceFactory())
        login_as(self.user, self)
        response = self.client.get("%s?forward=%s" % (
            reverse('combination-autocomplete'),
            json.dumps({"subject_only": obj.subject.id, })))
        self.assertContains(response, strip_tags(obj.contents)[0:25])
        self.assertContains(response, obj.pk)
        self.assertNotContains(response, strip_tags(obj2.contents)[0:25])

    def test_list_subjects(self):
        obj = SubjectFactory()
        login_as(self.user, self)
        response = self.client.get(reverse('subject-autocomplete'))
        self.assertContains(response, obj.name)
        self.assertContains(response, obj.pk)

    def test_no_access_subjects(self):
        obj = SubjectFactory()
        response = self.client.get(reverse('subject-autocomplete'))
        self.assertNotContains(response, obj.name)
        self.assertNotContains(response, obj.pk)

    def test_list_subjects_w_search(self):
        obj = SubjectFactory(name="special stuff")
        obj2 = SubjectFactory()
        login_as(self.user, self)
        response = self.client.get("%s?q=%s" % (
            reverse('subject-autocomplete'),
            "special"))
        self.assertContains(response, obj.name)
        self.assertContains(response, obj.pk)
        self.assertNotContains(response, obj2.name)

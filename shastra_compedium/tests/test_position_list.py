from django.test import TestCase
from django.test import Client
from django.urls import reverse
from shastra_compedium.tests.factories import (
    PositionDetailFactory,
    SourceFactory,
    UserFactory
)
from shastra_compedium.tests.functions import login_as


class TestPositionList(TestCase):
    view_name = "position_list"

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.source = SourceFactory()
        self.detail = PositionDetailFactory(usage="Meaning")
        self.detail.sources.add(self.source)
        self.detail.save()
        self.url = reverse(self.view_name, urlconf="shastra_compedium.urls")

    def test_list_positions_basic(self):
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, self.detail.position.name)
        self.assertContains(response, reverse(
            "position-update",
            urlconf="shastra_compedium.urls",
            args=[self.detail.position.pk]))
        self.assertContains(
            response,
            '<a href="%s" class="nav-link active">Position List</a>' % (
                self.url),
            html=True)

    def test_list_categories_all_the_things(self):
        another_detail = PositionDetailFactory(
            position=self.detail.position,
            usage="Posture Description")
        another_source_detail = PositionDetailFactory(
            position=self.detail.position,
            usage="Posture Description")
        another_detail.sources.add(self.source)
        another_source = SourceFactory()
        another_source_detail.sources.add(another_source)
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, "'id': %d" % self.detail.position.pk)
        self.assertContains(response,
                            "'position': '%s'" % self.detail.position.name)
        self.assertContains(
            response,
            ('<th data-field="%s_Posture Description" data-sortable="false">' +
             '%s Description</th>') % (self.source.title, self.source.title))
        self.assertContains(
            response,
            ('<th data-field="%s_Meaning" data-sortable="false">' +
             '%s Meaning</th>') % (self.source.title,
                                   self.source.title))
        self.assertContains(
            response,
            ('<th data-field="%s_Posture Description" data-sortable="false">' +
             '%s Description</th>') % (another_source.title,
                                       another_source.title))
        self.assertContains(
            response,
            ('%s&nbsp;&nbsp;<a class="lakshmi-detail" href="%s?next=%s" ' +
             'title="Edit"><i class="fas fa-edit"></i></a>') % (
             self.detail.position.category,
             reverse("category-update",
                     urlconf="shastra_compedium.urls",
                     args=[self.detail.position.category.pk]),
             self.url))
        self.assertContains(
            response,
            ('<a class="lakshmi-detail" href="%s" title="Edit"><i ' +
             'class="fas fa-edit"></i></a>') % (
             reverse("position-update",
                     urlconf="shastra_compedium.urls",
                     args=[self.detail.position.pk])))
        self.assertContains(
            response,
            "'%s_%s': '%s'" % (
                self.source,
                self.detail.usage,
                self.detail.contents))
        self.assertContains(
            response,
            "'%s_%s': '%s'" % (
                self.source,
                another_detail.usage,
                another_detail.contents))
        self.assertContains(
            response,
            "'%s_%s': '%s'" % (
                another_source,
                another_source_detail.usage,
                another_source_detail.contents))

    def test_list_empty(self):
        ex_url = reverse(
            "position-update",
            urlconf="shastra_compedium.urls",
            args=[self.detail.pk])
        self.detail.delete()
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertNotContains(response, ex_url)
        self.assertNotContains(response, "'action':")

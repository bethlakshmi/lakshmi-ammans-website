from django.test import TestCase
from django.test import Client
from django.urls import reverse
from shastra_compedium.tests.factories import (
    PositionDetailFactory,
    SourceFactory,
    UserFactory
)
from shastra_compedium.models import PositionDetail
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
        another_meaning = PositionDetailFactory(
            position=self.detail.position,
            usage="Meaning",
            chapter=1,
            verse_start=2,
            verse_end=3)
        another_source_detail = PositionDetailFactory(
            position=self.detail.position,
            usage="Posture Description")
        another_detail.sources.add(self.source)
        another_meaning.sources.add(self.source)
        another_source = SourceFactory()
        another_source_detail.sources.add(another_source)
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, "'id': %d" % self.detail.position.pk)
        self.assertContains(response,
                            "'position': '%s'" % self.detail.position.name)
        header = ('<th data-field="%d" data-sortable="false"><span title=' +
                  '"%s - %s">%s<br>%s</span></th>')
        self.assertContains(
            response,
            header % (self.source.pk,
                      self.source.title,
                      self.source.translator,
                      self.source.shastra.initials,
                      self.source.short_form
                      ),
            html=True)
        self.assertContains(
            response,
            header % (another_source.pk,
                      another_source.title,
                      another_source.translator,
                      another_source.shastra.initials,
                      another_source.short_form),
            html=True)
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
        source_cell = (
            '\'%s\': \'<a class="lakshmi-text-success" href="#" data-toggle=' +
            '"modal" data-target="#Modal%s_%s" data-backdrop="true" ><i ' +
            'class="far fa-check-square fa-2x"></i></a>\'')
        self.assertContains(
            response,
            source_cell % (
                self.source.pk,
                self.source.pk,
                self.detail.position.pk))
        self.assertContains(
            response,
            source_cell % (
                self.source.pk,
                self.source.pk,
                another_detail.position.pk))
        self.assertContains(
            response,
            source_cell % (
                another_source.pk,
                another_source.pk,
                another_source_detail.position.pk))
        self.assertContains(response, "1:2-3")
        self.assertContains(response, "No associated description")
        self.assertContains(response, "No associated meanings")
        self.assertContains(response, 'rowspan="3"')

    def test_list_linked_posture_meaning(self):
        PositionDetail.objects.all().delete()
        another_detail = PositionDetailFactory(
            position=self.detail.position,
            usage="Posture Description")
        another_meaning = PositionDetailFactory(
            position=self.detail.position,
            description=another_detail,
            usage="Meaning",
            chapter=1,
            verse_start=2,
            verse_end=3)
        another_detail.sources.add(self.source)
        another_meaning.sources.add(self.source)
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, "'id': %d" % self.detail.position.pk)
        self.assertContains(response,
                            "'position': '%s'" % self.detail.position.name)
        header = ('<th data-field="%d" data-sortable="false"><span title=' +
                  '"%s - %s">%s<br>%s</span></th>')
        self.assertContains(
            response,
            header % (self.source.pk,
                      self.source.title,
                      self.source.translator,
                      self.source.shastra.initials,
                      self.source.short_form
                      ),
            html=True)
        self.assertContains(response, 'rowspan="1"')
        self.assertContains(response, another_detail.contents)
        self.assertContains(response, another_meaning.contents)
        self.assertNotContains(response, "No associated description")
        self.assertNotContains(response, "No associated meanings")

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

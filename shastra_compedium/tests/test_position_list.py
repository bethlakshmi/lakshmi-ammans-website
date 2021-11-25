from django.test import TestCase
from django.test import Client
from django.urls import reverse
from shastra_compedium.tests.factories import (
    ExampleImageFactory,
    PositionDetailFactory,
    SourceFactory,
    UserFactory
)
from shastra_compedium.models import PositionDetail
from shastra_compedium.tests.functions import (
    login_as,
    set_image
)
from easy_thumbnails.files import get_thumbnailer


class TestPositionList(TestCase):
    view_name = "position_list"
    options = {'size': (350, 350), 'crop': False}

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
            'class="far fa-check-square fa-4x"></i></a>\'')
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

    def test_main_image(self):
        img1 = set_image()
        example_image = ExampleImageFactory(image=img1, general=True)
        login_as(self.user, self)
        response = self.client.get(self.url)
        thumb_url = get_thumbnailer(img1).get_thumbnail(self.options).url
        self.assertContains(response, thumb_url)

    def test_posture_image(self):
        another_detail = PositionDetailFactory(
            position=self.detail.position,
            usage="Posture Description")
        another_detail.sources.add(self.source)
        another_detail.save()
        img1 = set_image()
        example_image = ExampleImageFactory(
            image=img1,
            position=another_detail.position)
        example_image.details.add(another_detail)
        login_as(self.user, self)
        response = self.client.get(self.url)
        thumb_url = get_thumbnailer(img1).get_thumbnail(self.options).url
        self.assertContains(response, thumb_url)

    def test_meaning_image(self):
        img1 = set_image()
        example_image = ExampleImageFactory(
            image=img1,
            position=self.detail.position)
        example_image.details.add(self.detail)
        login_as(self.user, self)
        response = self.client.get(self.url)
        thumb_url = get_thumbnailer(img1).get_thumbnail(self.options).url
        self.assertContains(response, thumb_url)

    def test_meaning_w_description_image(self):
        another_detail = PositionDetailFactory(
            position=self.detail.position,
            usage="Posture Description")
        another_detail.sources.add(self.source)
        another_detail.save()
        self.detail.description = another_detail
        self.detail.save()
        img1 = set_image()
        example_image = ExampleImageFactory(
            image=img1,
            position=self.detail.position)
        example_image.details.add(self.detail)
        login_as(self.user, self)
        response = self.client.get(self.url)
        print(self.detail.position.name)
        print(self.detail.contents)
        print(self.detail.exampleimage_set.first())
        print(self.detail.exampleimage_set.first().general)

        print(response.content)
        thumb_url = get_thumbnailer(img1).get_thumbnail(self.options).url
        self.assertContains(response, thumb_url)
        self.assertNotContains(response, "No associated description")

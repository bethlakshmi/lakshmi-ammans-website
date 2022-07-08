from django.test import TestCase
from django.urls import reverse
from django.test import Client
from shastra_compedium.tests.factories import (
    CategoryDetailFactory,
    CombinationDetailFactory,
    ExampleImageFactory,
    PositionDetailFactory,
    SourceFactory,
    UserFactory,
)
from shastra_compedium.tests.functions import (
    login_as,
    set_image,
)
from shastra_compedium.models import Performer
from easy_thumbnails.files import get_thumbnailer


class TestShastraChapter(TestCase):

    view_name = 'shastrachapter-view'
    update_name = 'position-detail-update'
    options = {'size': (350, 350), 'crop': False}

    def setUp(self):
        self.client = Client()
        self.source = SourceFactory()
        self.chapter_detail = CategoryDetailFactory(chapter=4)
        self.chapter_detail.sources.add(self.source)
        self.view_url = reverse(self.view_name,
                                args=[self.source.shastra.pk,
                                      self.chapter_detail.category.pk],
                                urlconf='shastra_compedium.urls')
        self.cat_edit_url = reverse("category-update",
                                    args=[self.chapter_detail.category.pk],
                                    urlconf='shastra_compedium.urls')
        self.source_edit_url = reverse(
            "shastra-update",
            args=[self.source.shastra.pk],
            urlconf='shastra_compedium.urls')
        self.user = UserFactory()

    def test_view_w_login(self):
        login_as(self.user, self)
        response = self.client.get(self.view_url)
        self.assertContains(response, '%s: %s (%s)' % (
            self.source.shastra,
            self.chapter_detail.category,
            self.chapter_detail.category.summary))
        self.assertContains(response, self.cat_edit_url)
        self.assertContains(response, self.source_edit_url)

    def test_view_no_login(self):
        response = self.client.get(self.view_url)
        self.assertContains(response, '%s: %s (%s)' % (
            self.source.shastra,
            self.chapter_detail.category,
            self.chapter_detail.category.summary))
        self.assertNotContains(response, self.cat_edit_url)
        self.assertNotContains(response, self.source_edit_url)

    def test_edit_wrong_source(self):
        response = self.client.get(reverse(
            self.view_name,
            args=[self.source.shastra.pk+100, self.chapter_detail.category.pk],
            urlconf='shastra_compedium.urls'))
        self.assertEqual(404, response.status_code)

    def test_edit_wrong_category(self):
        response = self.client.get(reverse(
            self.view_name,
            args=[self.source.shastra.pk, self.chapter_detail.category.pk+100],
            urlconf='shastra_compedium.urls'))
        self.assertEqual(404, response.status_code)

    def test_posture_and_meaning(self):
        another_detail = PositionDetailFactory(
            usage="Posture Description",
            position__category=self.chapter_detail.category)
        another_meaning = PositionDetailFactory(
            position=another_detail.position,
            description=another_detail,
            usage="Meaning",
            chapter=1,
            verse_start=2,
            verse_end=3)
        another_detail.sources.add(self.source)
        another_meaning.sources.add(self.source)
        response = self.client.get(self.view_url)
        self.assertContains(response, another_detail.position.name)
        self.assertContains(response, self.source.title)
        self.assertContains(response, another_detail.contents)
        self.assertContains(response, another_meaning.verses())

    def test_description_image(self):
        another_detail = PositionDetailFactory(
            usage="Posture Description",
            position__category=self.chapter_detail.category)
        img1 = set_image()
        example_image = ExampleImageFactory(
            image=img1,
            general=True,
            position=another_detail.position)
        example_image.details.add(another_detail)
        another_detail.sources.add(self.source)
        response = self.client.get(self.view_url)
        thumb_url = get_thumbnailer(img1).get_thumbnail(self.options).url
        self.assertContains(response, thumb_url)

    def test_combination(self):
        another_detail = PositionDetailFactory(
            usage="Posture Description",
            position__category=self.chapter_detail.category)
        combo1 = CombinationDetailFactory(
            positions=[another_detail.position],
            chapter=self.chapter_detail.chapter)
        combo2 = CombinationDetailFactory(
            positions=[another_detail.position],
            chapter=self.chapter_detail.chapter)
        combo1.sources.add(self.source)
        combo2.sources.add(self.source)
        another_detail.sources.add(self.source)
        img1 = set_image()
        example_image = ExampleImageFactory(
            image=img1)
        example_image.combinations.add(combo1)
        response = self.client.get(self.view_url)
        thumb_url = get_thumbnailer(img1).get_thumbnail(self.options).url
        self.assertContains(response, thumb_url)
        self.assertContains(response, combo1.contents)
        self.assertContains(response, combo2.contents)
        thumb_url = get_thumbnailer(img1).get_thumbnail(self.options).url
        self.assertContains(response, thumb_url)
        self.assertContains(response, "No associated images")


    def test_combination_w_position_image(self):
        another_detail = PositionDetailFactory(
            usage="Posture Description",
            position__category=self.chapter_detail.category)
        another_detail.sources.add(self.source)
        img1 = set_image()
        example_image = ExampleImageFactory(
            image=img1,
            general=True,
            position=another_detail.position)
        combo1 = CombinationDetailFactory(
            positions=[another_detail.position],
            chapter=self.chapter_detail.chapter)
        combo1.sources.add(self.source)
        example_image.details.add(another_detail)

        response = self.client.get(self.view_url)
        self.assertContains(response, "%s#%d_%d" % (
            reverse("position-view",
                    urlconf='shastra_compedium.urls',
                    args=[another_detail.position.pk]),
            self.source.pk,
            another_detail.position.pk))

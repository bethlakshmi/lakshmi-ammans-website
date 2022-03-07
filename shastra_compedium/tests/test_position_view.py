from django.test import TestCase
from django.urls import reverse
from django.test import Client
from shastra_compedium.tests.factories import (
    ExampleImageFactory,
    PositionDetailFactory,
    PositionFactory,
    SourceFactory,
    UserFactory,
)
from shastra_compedium.tests.functions import (
    login_as,
    set_image,
)
from easy_thumbnails.files import get_thumbnailer


class TestViewPosition(TestCase):

    view_name = 'position-view'
    update_name = 'position-detail-update'
    options = {'size': (350, 350), 'crop': False}
    options2 = {'size': (150, 150), 'crop': False}
    options3 = {'size': (50, 50), 'crop': False}

    def setUp(self):
        self.client = Client()
        self.object = PositionFactory()
        self.view_url = reverse(self.view_name,
                                args=[self.object.pk],
                                urlconf='shastra_compedium.urls')
        self.edit_url = reverse(self.update_name,
                                args=[self.object.pk],
                                urlconf='shastra_compedium.urls')
        self.user = UserFactory()

    def test_view_w_login(self):
        login_as(self.user, self)
        response = self.client.get(self.view_url)
        self.assertContains(response, self.object.name)
        self.assertContains(response, self.edit_url)

    def test_view_no_login(self):
        response = self.client.get(self.view_url)
        self.assertContains(response, self.object.name)
        self.assertNotContains(response, self.edit_url)

    def test_edit_wrong_position(self):
        response = self.client.get(reverse(self.view_name,
                                args=[self.object.pk+100],
                                urlconf='shastra_compedium.urls'))
        self.assertEqual(404, response.status_code)

    def test_view_many_things(self):
        img1 = set_image()
        self.example_image = ExampleImageFactory(
            image=img1,
            general=True,
            position=self.object)
        response = self.client.get(self.view_url)
        self.assertContains(response, self.object.name)
        self.assertNotContains(response, self.edit_url)
        thumb_url = get_thumbnailer(img1).get_thumbnail(self.options).url
        self.assertContains(response, thumb_url)
        self.assertContains(response, reverse(
            "dancestyle-view",
            args=[self.example_image.dance_style.pk],
            urlconf='shastra_compedium.urls'))
        self.assertContains(response, reverse(
            "performer-view",
            args=[self.example_image.performer.pk],
            urlconf='shastra_compedium.urls'))

    def test_posture_and_meaning(self):
        self.source = SourceFactory()
        another_detail = PositionDetailFactory(
            position=self.object,
            usage="Posture Description")
        another_meaning = PositionDetailFactory(
            position=self.object,
            description=another_detail,
            usage="Meaning",
            chapter=1,
            verse_start=2,
            verse_end=3)
        another_detail.sources.add(self.source)
        another_meaning.sources.add(self.source)
        response = self.client.get(self.view_url)
        self.assertContains(response, '<a id="%d_%d"></a>' % (
            self.source.pk,
            self.object.pk))
        self.assertContains(response, another_detail.contents)
        self.assertContains(response, another_meaning.verses())
        self.assertContains(response, "<i>No associated images</i>")
        self.assertNotContains(response, "<i>No associated meanings</i>")
        self.assertNotContains(response, "<i>No associated description</i>")
        self.assertNotContains(response, "<b>Based upon:</b>")

    def test_posture_and_meaning_disconnected(self):
        self.source = SourceFactory()
        another_detail = PositionDetailFactory(
            position=self.object,
            usage="Posture Description")
        another_meaning = PositionDetailFactory(
            position=self.object,
            usage="Meaning",
            chapter=1,
            verse_start=2,
            verse_end=3)
        another_detail.sources.add(self.source)
        another_meaning.sources.add(self.source)
        response = self.client.get(self.view_url)
        self.assertContains(response, another_detail.contents)
        self.assertContains(response, another_meaning.verses())
        self.assertContains(response, "<i>No associated images</i>")
        self.assertContains(response, "<i>No associated meanings</i>")
        self.assertContains(response, "<i>No associated description</i>")

    def test_2_postures_1_position(self):
        self.source = SourceFactory()
        another_detail = PositionDetailFactory(
            position=self.object,
            usage="Posture Description")
        second_detail = PositionDetailFactory(
            position=self.object,
            usage="Posture Description")
        another_detail.sources.add(self.source)
        second_detail.sources.add(self.source)
        response = self.client.get(self.view_url)
        self.assertContains(response, '<a id="%d_%d"></a>' % (
            self.source.pk,
            self.object.pk))
        self.assertContains(response, another_detail.contents)
        self.assertContains(response, second_detail.verses())
        self.assertContains(response, "<i>No associated images</i>", 2)
        self.assertContains(response, "<i>No associated meanings</i>", 2)

    def test_meaning_only(self):
        self.source = SourceFactory()
        another_meaning = PositionDetailFactory(
            position=self.object,
            usage="Meaning",
            chapter=1,
            verse_start=2,
            verse_end=3)
        another_meaning.sources.add(self.source)
        response = self.client.get(self.view_url)
        self.assertContains(response, '<a id="%d_%d"></a>' % (
            self.source.pk,
            self.object.pk))
        self.assertContains(response, another_meaning.verses())
        self.assertContains(response, "<i>No associated description</i>")

    def test_dependency(self):
        self.source = SourceFactory()
        dependancy = PositionDetailFactory(
            usage="Posture Description")
        img1 = set_image()
        example_image = ExampleImageFactory(
            image=img1,
            general=True,
            position=dependancy.position)

        another_detail = PositionDetailFactory(
            position=self.object,
            usage="Posture Description",)
        another_meaning = PositionDetailFactory(
            position=self.object,
            description=another_detail,
            usage="Meaning",
            chapter=1,
            verse_start=2,
            verse_end=3)
        example_image.details.add(dependancy)
        dependancy.sources.add(self.source)
        another_detail.sources.add(self.source)
        another_detail.dependencies.add(dependancy)
        another_meaning.sources.add(self.source)
        response = self.client.get(self.view_url)
        self.assertContains(response, "<b>Based upon:</b>")
        self.assertContains(response, "%s#%d_%d" % (
            reverse(self.view_name,
                    args=[dependancy.position.pk],
                    urlconf='shastra_compedium.urls'),
            self.source.pk,
            dependancy.position.pk))
        thumb_url = get_thumbnailer(img1).get_thumbnail(self.options2).url
        self.assertContains(response, thumb_url)

    def test_dependedupon(self):
        self.source = SourceFactory()
        dependancy = PositionDetailFactory(
            usage="Posture Description")
        img1 = set_image()
        example_image = ExampleImageFactory(
            image=img1,
            general=True,
            position=dependancy.position)

        another_detail = PositionDetailFactory(
            position=self.object,
            usage="Posture Description",)
        another_meaning = PositionDetailFactory(
            position=self.object,
            description=another_detail,
            usage="Meaning",
            chapter=1,
            verse_start=2,
            verse_end=3)
        example_image.details.add(dependancy)
        dependancy.sources.add(self.source)
        another_detail.sources.add(self.source)
        dependancy.dependencies.add(another_detail)
        another_meaning.sources.add(self.source)
        response = self.client.get(self.view_url)
        print(response.content)
        self.assertContains(response, "<b>Mentioned by:</b>")
        self.assertContains(response, "%s#%d_%d" % (
            reverse(self.view_name,
                    args=[dependancy.position.pk],
                    urlconf='shastra_compedium.urls'),
            self.source.pk,
            dependancy.position.pk))
        thumb_url = get_thumbnailer(img1).get_thumbnail(self.options3).url
        self.assertContains(response, thumb_url)

    def test_description_image(self):
        self.source = SourceFactory()

        another_detail = PositionDetailFactory(
            position=self.object,
            usage="Posture Description",)
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
        self.assertContains(response, "<i>No associated meanings</i>")

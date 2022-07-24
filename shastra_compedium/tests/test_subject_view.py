from django.test import TestCase
from django.urls import reverse
from django.test import Client
from shastra_compedium.tests.factories import (
    CombinationDetailFactory,
    ExampleImageFactory,
    SourceFactory,
    UserFactory,
)
from shastra_compedium.tests.combo_context import CombinationContext
from shastra_compedium.tests.functions import (
    login_as,
    set_image,
)
from easy_thumbnails.files import get_thumbnailer


class TestViewSubject(TestCase):

    view_name = 'subject-view'
    update_name = 'subject-update'
    options = {'size': (350, 350), 'crop': False}
    options2 = {'size': (150, 150), 'crop': False}
    options3 = {'size': (50, 50), 'crop': False}

    def setUp(self):
        self.client = Client()
        self.context = CombinationContext()
        self.object = self.context.combo.subject
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
        self.assertContains(response, self.object.category.name)
        self.assertContains(response, self.edit_url)
        self.assertContains(response, "<i>No image available</i>", html=True)

    def test_view_no_login(self):
        response = self.client.get(self.view_url)
        self.assertContains(response, self.object.name)
        self.assertNotContains(response, self.edit_url)
        self.assertContains(response, "<i>No image available</i>", html=True)

    def test_edit_wrong_object(self):
        response = self.client.get(reverse(self.view_name,
                                   args=[self.object.pk+100],
                                   urlconf='shastra_compedium.urls'))
        self.assertEqual(404, response.status_code)

    def test_view_direct_images(self):
        self.context.set_images()
        response = self.client.get(self.view_url)
        thumb_url = get_thumbnailer(self.context.img1).get_thumbnail(
            self.options).url
        self.assertContains(response, thumb_url)
        self.assertContains(response, reverse(
            "dancestyle-view",
            args=[self.context.example_image.dance_style.pk],
            urlconf='shastra_compedium.urls'))
        self.assertContains(response, reverse(
            "performer-view",
            args=[self.context.example_image2.performer.pk],
            urlconf='shastra_compedium.urls'))
        self.assertContains(response, self.context.img2.url)

    def test_pos_detail_images(self):
        self.context.set_dependancies()
        response = self.client.get(self.view_url)
        self.assertContains(response, "<b>Based upon:</b>")
        self.assertContains(response, "%s#%d_%d" % (
            reverse("position-view",
                    args=[self.context.first_position.pk],
                    urlconf='shastra_compedium.urls'),
            self.context.source.pk,
            self.context.first_position.pk))
        thumb_url = get_thumbnailer(self.context.pos_img).get_thumbnail(
            self.options2).url
        self.assertContains(response, thumb_url)
        self.assertContains(response, self.context.first_position.name)

    def test_no_positions(self):
        context = CombinationContext()
        for pos in context.combo.positions.all():
            context.combo.positions.remove(pos)
        self.view_url = reverse(self.view_name,
                                args=[context.combo.subject.pk],
                                urlconf='shastra_compedium.urls')
        response = self.client.get(self.view_url)
        self.assertContains(response, context.combo.subject.name)
        print(response.content)
        self.assertContains(response, "<i>No dependencies</i>", html=True)

    def test_pos_detail_no_image(self):
        self.context.set_dependancies(setup_image=False)
        response = self.client.get(self.view_url)
        self.assertContains(response, "<b>Based upon:</b>")
        self.assertContains(response, "<i>No image available</i>", html=True)
        self.assertContains(response, self.context.first_position.name)
        self.assertContains(response, "%s#%d_%d" % (
            reverse("position-view",
                    args=[self.context.first_position.pk],
                    urlconf='shastra_compedium.urls'),
            self.context.source.pk,
            self.context.first_position.pk))

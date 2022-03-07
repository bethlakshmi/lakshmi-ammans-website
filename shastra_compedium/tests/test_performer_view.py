from django.test import TestCase
from django.urls import reverse
from django.test import Client
from shastra_compedium.tests.factories import (
    DanceStyleFactory,
    PerformerFactory,
    UserFactory,
)
from shastra_compedium.tests.functions import (
    login_as,
    set_image,
)
from easy_thumbnails.files import get_thumbnailer


class TestViewPerformer(TestCase):

    view_name = 'performer-view'
    update_name = 'performer-update'
    options = {'size': (350, 350), 'crop': False}

    def setUp(self):
        self.client = Client()
        self.dance_style = DanceStyleFactory()
        self.object = PerformerFactory(dance_styles=[self.dance_style])
        self.view_url = reverse(self.view_name,
                                args=[self.object.pk],
                                urlconf='shastra_compedium.urls')
        self.edit_url = reverse(self.update_name,
                                args=[self.object.pk],
                                urlconf='shastra_compedium.urls')
        self.user = UserFactory()

    def test_view_w_login(self):
        img1 = set_image()
        self.object.image = img1
        self.object.save()
        login_as(self.user, self)
        response = self.client.get(self.view_url)
        self.assertContains(response, self.object.name)
        self.assertContains(response, self.object.linneage)
        self.assertContains(response, self.object.bio)
        self.assertContains(response, self.edit_url)
        thumb_url = get_thumbnailer(img1).get_thumbnail(self.options).url
        self.assertContains(response, thumb_url)
        self.assertContains(response, reverse(
            "dancestyle-view",
            args=[self.dance_style.pk],
            urlconf='shastra_compedium.urls'))

    def test_view_no_login(self):
        response = self.client.get(self.view_url)
        self.assertContains(response, self.object.name)
        self.assertNotContains(response, self.edit_url)

    def test_edit_wrong_performer(self):
        response = self.client.get(reverse(self.view_name,
                                args=[self.object.pk+100],
                                urlconf='shastra_compedium.urls'))
        self.assertEqual(404, response.status_code)

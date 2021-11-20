from django.test import TestCase
from django.urls import reverse
from django.test import Client
from shastra_compedium.tests.factories import (
    ExampleImageFactory,
    UserFactory,
)
from shastra_compedium.site_text import make_example_image_messages
from shastra_compedium.tests.functions import (
    login_as,
    set_image
)
from easy_thumbnails.files import get_thumbnailer
from shastra_compedium.models import ExampleImage


class TestMakeExampleImage(TestCase):
    '''Tests for Example Image create & update'''

    update_name = 'exampleimage-update'
    options = {'size': (200, 200), 'crop': False}

    def setUp(self):
        self.client = Client()
        self.img1 = set_image()
        self.object = ExampleImageFactory(image=self.img1)
        self.edit_url = reverse(self.update_name,
                                args=[self.object.pk],
                                urlconf='shastra_compedium.urls')
        user = UserFactory()
        login_as(user, self)

    def example_image_data(self):
        return {'image': self.img1.pk,
                'performer': self.object.performer.pk,
                'dance_style': self.object.dance_style.pk,
                'position': self.object.position.pk,
                'general': True,
                'details': []}

    def test_get_edit_get(self):
        response = self.client.get(self.edit_url)
        self.assertContains(response, "Update Example Image")
        self.assertContains(response,
                            make_example_image_messages['edit_intro'])
        self.assertContains(response, "Main Image?")
        thumb_url = get_thumbnailer(self.img1).get_thumbnail(self.options).url
        self.assertContains(response, thumb_url)

    def test_edit_post(self):
        start = ExampleImage.objects.all().count()
        response = self.client.post(self.edit_url,
                                    data=self.example_image_data(),
                                    follow=True)
        self.assertContains(
            response,
            make_example_image_messages['edit_success'] % str(self.object))
        self.assertEqual(start, ExampleImage.objects.all().count())

    def test_edit_error(self):
        from shastra_compedium.forms.default_form_text import item_image_help
        data = self.example_image_data()
        data['general'] = False
        response = self.client.post(self.edit_url, data=data, follow=True)
        self.assertNotContains(
            response,
            make_example_image_messages['edit_success'] % str(self.object))
        self.assertContains(response, item_image_help['general_or_details'])
        self.assertContains(response,
                            make_example_image_messages['edit_intro'])
        thumb_url = get_thumbnailer(self.img1).get_thumbnail(self.options).url
        self.assertContains(response, thumb_url)

from django.test import TestCase
from django.urls import reverse
from django.test import Client
from shastra_compedium.tests.factories import (
    CombinationDetailFactory,
    ExampleImageFactory,
    PositionFactory,
    PositionDetailFactory,
    UserFactory,
)
from shastra_compedium.site_text import make_example_image_messages
from shastra_compedium.tests.functions import (
    login_as,
    set_image
)
from easy_thumbnails.files import get_thumbnailer
from shastra_compedium.models import ExampleImage
from django.urls import reverse


class TestMakeExampleImage(TestCase):
    '''Tests for Example Image create & update'''

    update_name = 'exampleimage-update'
    create_name = 'exampleimage-add'
    copy_name = 'exampleimage-copy'
    options = {'size': (200, 200), 'crop': False}

    def setUp(self):
        self.client = Client()
        self.img1 = set_image()
        self.img2 = set_image()
        self.object = ExampleImageFactory(image=self.img1)
        self.edit_url = reverse(self.update_name,
                                args=[self.object.pk],
                                urlconf='shastra_compedium.urls')
        self.create_url = reverse(self.create_name,
                                  args=[self.img2.pk],
                                  urlconf='shastra_compedium.urls')
        self.copy_url = reverse(self.copy_name,
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

    def test_edit_get(self):
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

    def test_change_position(self):
        new_position = PositionFactory()
        detail = PositionDetailFactory(position=self.object.position)
        self.object.details.add(detail)
        data = self.example_image_data()
        data['details'] = [detail.pk]
        data['position'] = new_position.pk
        self.assertEqual(detail.exampleimage_set.all().count(), 1)
        response = self.client.post(self.edit_url, data=data, follow=True)
        self.assertContains(response, self.object.image)
        self.assertRedirects(
            response,
            '%s?changed_ids=[%d]&obj_type=ExampleImage' % (
                reverse('image_list', urlconf="shastra_compedium.urls"),
                self.img1.pk))

    def test_keep_position(self):
        detail = PositionDetailFactory(position=self.object.position)
        self.object.details.add(detail)
        data = self.example_image_data()
        data['details'] = [detail.pk]
        self.assertEqual(detail.exampleimage_set.all().count(), 1)
        response = self.client.post(self.edit_url, data=data, follow=True)
        self.assertEqual(detail.exampleimage_set.all().count(), 1)
        self.assertContains(
            response,
            make_example_image_messages['edit_success'] % str(self.object))

    def test_create_get(self):
        response = self.client.get(self.create_url)
        self.assertContains(response, 'Create Example Image')
        self.assertContains(response,
                            make_example_image_messages['create_intro'])
        self.assertContains(response, "Main Image?")
        thumb_url = get_thumbnailer(self.img2).get_thumbnail(self.options).url
        self.assertContains(response, thumb_url)

    def test_create_post(self):
        start = ExampleImage.objects.all().count()
        data = self.example_image_data()
        data['image'] = self.img2.pk
        response = self.client.post(self.create_url,
                                    data=data,
                                    follow=True)
        self.assertContains(
            response,
            make_example_image_messages['create_success'] % (
                "Image %s, for Position %s," % (self.img2,
                                                self.object.position.name)))
        self.assertEqual(start+1, ExampleImage.objects.all().count())
        self.assertRedirects(
            response,
            '%s?changed_ids=[%d]&obj_type=ExampleImage' % (
                reverse('image_list', urlconf="shastra_compedium.urls"),
                self.img2.pk))

    def test_create_combo_only(self):
        start = ExampleImage.objects.all().count()
        data = self.example_image_data()
        combo = CombinationDetailFactory()
        data['image'] = self.img2.pk
        data['position'] = ""
        data['combinations'] = [combo.pk]
        response = self.client.post(self.create_url,
                                    data=data,
                                    follow=True)
        self.assertContains(
            response,
            make_example_image_messages['create_success'] % (
                "Image %s, with Combination Details," % self.img2))
        self.assertEqual(start+1, ExampleImage.objects.all().count())
        self.assertRedirects(
            response,
            '%s?changed_ids=[%d]&obj_type=ExampleImage' % (
                reverse('image_list', urlconf="shastra_compedium.urls"),
                self.img2.pk))

    def test_create_post_error(self):
        from shastra_compedium.forms.default_form_text import item_image_help
        detail = PositionDetailFactory(position=self.object.position)
        data = self.example_image_data()
        data['image'] = self.img2.pk
        data['details'] = [detail.pk]
        data['position'] = ""
        response = self.client.post(self.create_url,
                                    data=data,
                                    follow=True)
        self.assertNotContains(
            response,
            make_example_image_messages['create_success'] % (
                "Image %s, for Position %s," % (self.img2,
                                                self.object.position)))
        self.assertContains(response, item_image_help['pos_and_details'])

    def test_copy_get(self):
        response = self.client.get(self.copy_url)
        self.assertContains(response, 'Copy Image to a New Position')
        self.assertContains(response,
                            make_example_image_messages['copy_intro'])
        self.assertContains(response, "Main Image?")
        thumb_url = get_thumbnailer(self.img1).get_thumbnail(self.options).url
        self.assertContains(response, thumb_url)

    def test_copy_post(self):
        start = ExampleImage.objects.all().count()
        new_position = PositionFactory()
        data = {'image': self.img1.pk,
                'performer': self.object.performer.pk,
                'dance_style': self.object.dance_style.pk,
                'position': new_position.pk,
                'general': True,
                'details': []}
        response = self.client.post(self.copy_url,
                                    data=data,
                                    follow=True)
        self.assertContains(
            response,
            make_example_image_messages['copy_success'] % (
                "Image %s, for Position %s," % (self.img1, new_position.name)))
        self.assertEqual(start+1, ExampleImage.objects.all().count())
        self.assertRedirects(
            response,
            '%s?changed_ids=[%d]&obj_type=ExampleImage' % (
                reverse('image_list', urlconf="shastra_compedium.urls"),
                self.img1.pk))

    def test_copy_no_pos_no_combo(self):
        from shastra_compedium.forms.default_form_text import item_image_help
        start = ExampleImage.objects.all().count()
        new_position = PositionFactory()
        data = {'image': self.img1.pk,
                'performer': self.object.performer.pk,
                'dance_style': self.object.dance_style.pk,
                'position': "",
                'combinations': [],
                'general': True,
                'details': []}
        response = self.client.post(self.copy_url,
                                    data=data,
                                    follow=True)
        self.assertContains(
            response,
            item_image_help['position_or_combo'])

    def test_copy_post_error(self):
        data = self.example_image_data()
        response = self.client.post(self.copy_url,
                                    data=data,
                                    follow=True)
        self.assertNotContains(
            response,
            make_example_image_messages['copy_success'] % (
                "Image %s, for Position %s," % (self.img1,
                                                self.object.position)))
        self.assertContains(
            response,
            "Example image with this Image and Position already exists.")

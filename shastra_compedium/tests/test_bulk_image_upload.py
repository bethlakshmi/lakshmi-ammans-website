from django.test import TestCase
from django.test import Client
from django.urls import reverse
from shastra_compedium.tests.factories import (
    DanceStyleFactory,
    PerformerFactory,
    PositionFactory,
    ExampleImageFactory,
    UserFactory
)
from shastra_compedium.tests.functions import (
    login_as,
    set_image
)
from shastra_compedium.models import ExampleImage
from easy_thumbnails.files import get_thumbnailer
from filer.models import Image


class TestBulkImageUpload(TestCase):
    ''' This view reuses the generic wizard that is fully tested in
    make_item testing.  As such, this collection limits itself to
    what's special for bulk image upload - including a lot of multi-form
    logic'''
    view_name = "image_upload"
    options = {'size': (100, 100), 'crop': False}
    image_checkbox = '''<input type="checkbox" name="current_images"
        style="display: none;" id="id_current_images_%d" value="%d" %s>'''

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.itemimage = ExampleImageFactory()
        set_image(self.itemimage)
        self.url = reverse(self.view_name,
                           urlconf="shastra_compedium.urls")

    def test_get(self):
        from shastra_compedium.forms.default_form_text import item_image_help
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, item_image_help['new_images'])

    def test_upload_files_continue(self):
        UserFactory(username='admin_img')
        login_as(self.user, self)
        file1 = open("shastra_compedium/tests/redexpo.jpg", 'rb')
        file2 = open("shastra_compedium/tests/10yrs.jpg", 'rb')
        style = DanceStyleFactory()
        performer = PerformerFactory()
        response = self.client.post(
            self.url,
            data={'new_images': [file1, file2],
                  'default_performer': performer.pk,
                  'default_dance_style': style.pk,
                  'step': 0,
                  'next': 'Save & Continue >>'},
            follow=True)
        image2 = Image.objects.latest('pk')
        image1 = Image.objects.get(pk=image2.pk-1)
        thumb_url = get_thumbnailer(
            image1).get_thumbnail(self.options).url
        self.assertContains(
            response,
            "Connect Images to Positions")
        self.assertContains(
            response,
            "<img src='%s' title='%s'/>" % (
                thumb_url,
                image1))
        thumb_url = get_thumbnailer(
            image2).get_thumbnail(self.options).url
        self.assertContains(
            response,
            "<img src='%s' title='%s'/>" % (
                thumb_url,
                image2))
        self.assertContains(
            response,
            '<input type="hidden" name="step" value="1" id="id_step">',
            html=True)
        self.assertContains(
            response,
            '<input type="hidden" name="association_count" value="2" ' +
            'id="id_association_count">',
            html=True)

    def test_upload_files_finish(self):
        UserFactory(username='admin_img')
        login_as(self.user, self)
        file1 = open("shastra_compedium/tests/redexpo.jpg", 'rb')
        file2 = open("shastra_compedium/tests/10yrs.jpg", 'rb')
        style = DanceStyleFactory()
        performer = PerformerFactory()
        response = self.client.post(
            self.url,
            data={'new_images': [file1, file2],
                  'step': 0,
                  'default_performer': performer.pk,
                  'default_dance_style': style.pk,
                  'finish': 'Finish'},
            follow=True)
        self.assertContains(response, "Uploaded 2 images.")

    def test_post_attachments_and_finish(self):
        img1 = set_image(self.itemimage)
        img2 = set_image(self.itemimage)
        position = PositionFactory()
        style = DanceStyleFactory()
        performer = PerformerFactory()
        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'0-image': img1.pk,
                  '1-image': img2.pk,
                  '0-position': position.pk,
                  '1-position': position.pk,
                  '0-performer': performer.pk,
                  '1-performer': performer.pk,
                  '0-dance_style': style.pk,
                  '1-dance_style': style.pk,
                  'step': 1,
                  'association_count': 2,
                  'finish': 'Finish'},
            follow=True)
        self.assertContains(
            response,
            "Uploaded 2 images.")

    def test_post_attachments_bad_item(self):
        # This is legit if a user selects something that is then deleted
        # before they submit
        img1 = set_image(self.itemimage)
        position = PositionFactory()
        style = DanceStyleFactory()
        performer = PerformerFactory()
        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'0-image': img1.pk,
                  '0-position': position.pk+1,
                  '0-perforner': performer.pk,
                  '0-dance_style': style.pk,
                  'step': 1,
                  'association_count': 2,
                  'finish': 'Finish'},
            follow=True)
        self.assertContains(
            response,
            "That choice is not one of the available choices.")

    def test_post_attachments_bad_image(self):
        # The user would have to be hacking the form to do this.
        img1 = set_image(self.itemimage)
        position = PositionFactory()
        style = DanceStyleFactory()
        performer = PerformerFactory()
        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'0-image': img1.pk+100,
                  '0-position': position.pk,
                  '0-perforner': performer.pk,
                  '0-dance_style': style.pk,
                  'step': 1,
                  'association_count': 2,
                  'finish': 'Finish'},
            follow=True)
        self.assertContains(response, "There is an error on the form.", 1)

    def test_post_attachments_bad_association(self):
        # The user would have to be hacking the form to do this.
        img1 = set_image(self.itemimage)
        style = DanceStyleFactory()
        performer = PerformerFactory()
        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'0-image': img1.pk,
                  '0-position': "",
                  '0-perforner': performer.pk,
                  '0-dance_style': style.pk,
                  'step': 1,
                  'association_count': 2,
                  'finish': 'Finish'},
            follow=True)
        self.assertContains(response, "There is an error on the form.", 1)

    def test_post_attachments_and_continue(self):
        img1 = set_image(self.itemimage)
        img2 = set_image(self.itemimage)
        position = PositionFactory()
        style = DanceStyleFactory()
        performer = PerformerFactory()
        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'0-image': img1.pk,
                  '1-image': img2.pk,
                  '0-position': position.pk,
                  '1-position': position.pk,
                  '0-perforner': performer.pk,
                  '1-perforner': performer.pk,
                  '0-dance_style': style.pk,
                  '1-dance_style': style.pk,
                  'step': 1,
                  'association_count': 2,
                  'next': 'Save & Continue >>'},
            follow=True)
        self.assertContains(
            response,
            "Set Specific Position Details")

from django.test import TestCase
from django.test import Client
from django.urls import reverse
from shastra_compedium.tests.factories import (
    CombinationDetailFactory,
    DanceStyleFactory,
    PerformerFactory,
    PositionFactory,
    PositionDetailFactory,
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
from django.utils.safestring import mark_safe
from shastra_compedium.site_text import (
    image_modal,
    user_messages,
)


class TestBulkImageUpload(TestCase):
    ''' This view reuses the generic wizard that is fully tested in
    make_item testing.  As such, this collection limits itself to
    what's special for bulk image upload - including a lot of multi-form
    logic'''
    view_name = "image_upload"
    options = {'size': (100, 100), 'crop': False}
    image_checkbox = '''<input type="checkbox" name="current_images"
        style="display: none;" id="id_current_images_%d" value="%d" %s>'''
    options2 = {'size': (200, 200), 'crop': False}
    finish_message = "Uploaded %d images."

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        set_image()
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
            image_modal % (image1.pk,
                           thumb_url,
                           image1,
                           image1.pk,
                           image1.url))
        thumb_url = get_thumbnailer(
            image2).get_thumbnail(self.options).url
        self.assertContains(
            response,
            image_modal % (image2.pk,
                           thumb_url,
                           image2,
                           image2.pk,
                           image2.url))
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
        self.assertContains(response, self.finish_message % 2)
        self.assertRedirects(
            response,
            reverse("image_list", urlconf="shastra_compedium.urls"))

    def test_post_attachments_and_finish(self):
        img1 = set_image()
        img2 = set_image()
        position = PositionFactory()
        combo = CombinationDetailFactory()
        style = DanceStyleFactory()
        performer = PerformerFactory()
        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'0-image': img1.pk,
                  '1-image': img2.pk,
                  '0-position': position.pk,
                  '1-position': "",
                  '1-subject': combo.subject.pk,
                  '0-performer': performer.pk,
                  '1-performer': performer.pk,
                  '0-dance_style': style.pk,
                  '1-dance_style': style.pk,
                  'step': 1,
                  'association_count': 2,
                  'finish': 'Finish'},
            follow=True)
        example1 = ExampleImage.objects.get(image=img1)
        example2 = ExampleImage.objects.get(image=img2)
        self.assertContains(response, self.finish_message % 2)
        self.assertRedirects(
            response,
            "%s?changed_ids=%s&obj_type=ExampleImage" % (
                reverse("image_list", urlconf="shastra_compedium.urls"),
                str([example1.pk, example2.pk])))
        self.assertContains(response, combo.subject.name)

    def test_post_attachments_bad_item(self):
        # This is legit if a user selects something that is then deleted
        # before they submit
        img1 = set_image()
        position = PositionFactory()
        style = DanceStyleFactory()
        performer = PerformerFactory()
        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'0-image': img1.pk,
                  '0-position': position.pk+1,
                  '0-performer': performer.pk,
                  '0-dance_style': style.pk,
                  'step': 1,
                  'association_count': 1,
                  'finish': 'Finish'},
            follow=True)
        self.assertContains(
            response,
            "That choice is not one of the available choices.")

    def test_post_attachments_no_pos_or_subject(self):
        from shastra_compedium.forms.default_form_text import item_image_help
        # Need at least 1 - position or combo
        img1 = set_image()
        position = PositionFactory()
        style = DanceStyleFactory()
        performer = PerformerFactory()
        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'0-image': img1.pk,
                  '0-performer': performer.pk,
                  '0-dance_style': style.pk,
                  'step': 1,
                  'association_count': 1,
                  'finish': 'Finish'},
            follow=True)
        self.assertContains(
            response,
            item_image_help['position_or_subject'])

    def test_post_bad_meta_data(self):
        img1 = set_image()
        img2 = set_image()
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
                  'num_rows': 2,
                  'finish': 'Finish'},
            follow=True)
        self.assertContains(
            response,
            user_messages['NO_FORM_ERROR']['description'])

    def test_post_attachments_bad_image(self):
        # The user would have to be hacking the form to do this.
        img1 = set_image()
        position = PositionFactory()
        style = DanceStyleFactory()
        performer = PerformerFactory()
        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'0-image': img1.pk+100,
                  '0-position': position.pk,
                  '0-performer': performer.pk,
                  '0-dance_style': style.pk,
                  'step': 1,
                  'association_count': 1,
                  'finish': 'Finish'},
            follow=True)
        self.assertContains(response, "There is an error on the form.", 1)

    def test_post_attachments_bad_association(self):
        # The user would have to be hacking the form to do this.
        img1 = set_image()
        style = DanceStyleFactory()
        performer = PerformerFactory()
        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'0-image': img1.pk,
                  '0-position': "",
                  '0-performer': performer.pk,
                  '0-dance_style': style.pk,
                  'step': 1,
                  'association_count': 1,
                  'finish': 'Finish'},
            follow=True)
        self.assertContains(response, "There is an error on the form.", 1)

    def test_post_attachments_and_continue(self):
        # only the images with positions get moved on to configure position
        # details.  The images with combinations only get saved, but not
        # setup in this form.
        img1 = set_image()
        img2 = set_image()
        combo = CombinationDetailFactory()
        position = PositionFactory()
        style = DanceStyleFactory()
        performer = PerformerFactory()
        detail1 = PositionDetailFactory(position=position)
        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'0-image': img1.pk,
                  '1-image': img2.pk,
                  '0-position': position.pk,
                  '1-position': "",
                  '1-subject': combo.subject.pk,
                  '0-performer': performer.pk,
                  '1-performer': performer.pk,
                  '0-dance_style': style.pk,
                  '1-dance_style': style.pk,
                  'step': 1,
                  'association_count': 2,
                  'next': 'Save & Continue >>'},
            follow=True)
        thumb_url = get_thumbnailer(img1).get_thumbnail(self.options2).url
        self.assertContains(response, "Set Specific Details")
        self.assertContains(response, thumb_url)
        self.assertContains(response, detail1.contents)
        self.assertContains(response, img2.url)

    def test_post_subject_only_and_continue(self):
        # only the images with positions get moved on to configure position
        # details.  The images with combinations only get saved, but not
        # setup in this form.
        img1 = set_image()
        img2 = set_image()
        combo = CombinationDetailFactory()
        position = PositionFactory()
        style = DanceStyleFactory()
        performer = PerformerFactory()
        detail1 = PositionDetailFactory(position=position)
        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'0-image': img1.pk,
                  '1-image': img2.pk,
                  '0-position': "",
                  '1-position': "",
                  '0-subject': combo.subject.pk,
                  '1-subject': combo.subject.pk,
                  '0-performer': performer.pk,
                  '1-performer': performer.pk,
                  '0-dance_style': style.pk,
                  '1-dance_style': style.pk,
                  'step': 1,
                  'association_count': 2,
                  'next': 'Save & Continue >>'},
            follow=True)
        thumb_url = get_thumbnailer(img1).get_thumbnail(self.options2).url

        self.assertContains(response, "Set Specific Details")
        self.assertContains(response, thumb_url)
        self.assertContains(response, combo.contents, 2)
        self.assertContains(response, img2.url)

    def test_pick_details(self):
        img1 = set_image()
        example_image = ExampleImageFactory(image=img1)
        detail1 = PositionDetailFactory(position=example_image.position)

        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'form-0-id': example_image.pk,
                  'form-0-details': [detail1.pk],
                  'form-0-general': True,
                  'form-TOTAL_FORMS': 1,
                  'form-INITIAL_FORMS': 1,
                  'form-MIN_NUM_FORMS': 0,
                  'form-MAX_NUM_FORMS': 1000,
                  'step': 2,
                  'association_count': 1,
                  'finish': 'Finish'},
            follow=True)
        self.assertContains(response, self.finish_message % 1)
        result = ExampleImage.objects.get(pk=example_image.pk)
        self.assertTrue(detail1 in result.details.all())
        self.assertTrue(result.general)

    def test_pick_nothing_error(self):
        from shastra_compedium.forms.default_form_text import item_image_help
        img1 = set_image()
        example_image = ExampleImageFactory(image=img1)
        detail1 = PositionDetailFactory(position=example_image.position)

        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'form-0-id': example_image.pk,
                  'form-0-details': [],
                  'form-0-combinations': [],
                  'form-0-general': False,
                  'form-TOTAL_FORMS': 1,
                  'form-INITIAL_FORMS': 1,
                  'form-MIN_NUM_FORMS': 0,
                  'form-MAX_NUM_FORMS': 1000,
                  'step': 2,
                  'association_count': 1,
                  'finish': 'Finish'},
            follow=True)
        self.assertContains(
            response,
            item_image_help['general_or_details'])
        thumb_url = get_thumbnailer(img1).get_thumbnail(self.options2).url
        self.assertContains(
            response,
            "<img src='%s' title='%s'/>" % (thumb_url, img1),
            html=True)

    def test_pick_combos(self):
        img1 = set_image()
        detail1 = CombinationDetailFactory()
        example_image = ExampleImageFactory(image=img1,
                                            subject=detail1.subject)

        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'form-0-id': example_image.pk,
                  'form-0-combinations': [detail1.pk],
                  'form-0-general': False,
                  'form-TOTAL_FORMS': 1,
                  'form-INITIAL_FORMS': 1,
                  'form-MIN_NUM_FORMS': 0,
                  'form-MAX_NUM_FORMS': 1000,
                  'step': 2,
                  'association_count': 1,
                  'finish': 'Finish'},
            follow=True)
        self.assertContains(response, self.finish_message % 1)
        result = ExampleImage.objects.get(pk=example_image.pk)
        self.assertTrue(detail1 in result.combinations.all())
        self.assertFalse(result.general)

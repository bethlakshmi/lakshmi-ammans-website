from django.test import TestCase
from django.test import Client
from django.urls import reverse
from shastra_compedium.tests.factories import (
    CombinationDetailFactory,
    ExampleImageFactory,
    PositionDetailFactory,
    UserFactory
)
from shastra_compedium.models import ExampleImage
from shastra_compedium.tests.functions import (
    login_as,
    set_image
)
from filer.models.imagemodels import Image


class TestImageList(TestCase):
    view_name = "image_list"

    def setUp(self):
        ExampleImage.objects.all().delete()
        self.client = Client()
        self.user = UserFactory()
        self.img1 = set_image(folder_name="PositionImageUploads")
        self.example_image = ExampleImageFactory(image=self.img1, general=True)
        self.url = reverse(self.view_name, urlconf="shastra_compedium.urls")

    def test_list_positions_basic_no_login(self):
        response = self.client.get(self.url)
        self.assertContains(response, self.example_image.position.name)
        self.assertContains(response, self.img1.url)
        self.assertContains(
            response,
            '<i class="lakshmi-text-success far fa-check-square fa-2x"></i>')
        self.assertContains(
            response,
            '<a href="%s" class="nav-link active">Images</a>' % (
                self.url),
            html=True)
        self.assertNotContains(response, reverse(
            "exampleimage-update",
            args=[self.example_image.pk],
            urlconf="shastra_compedium.urls"))
        self.assertNotContains(response, reverse(
            "category-update",
            args=[self.example_image.position.category.pk],
            urlconf="shastra_compedium.urls"))
        self.assertNotContains(response, reverse(
            "exampleimage-update",
            urlconf="shastra_compedium.urls",
            args=[self.example_image.pk]))

    def test_list_image(self):
        login_as(self.user, self)
        self.img2 = set_image(folder_name="PositionImageUploads")
        response = self.client.get(self.url)
        self.assertContains(response, self.img2.url)
        self.assertContains(response, reverse(
            "exampleimage-add",
            urlconf="shastra_compedium.urls",
            args=[self.img2.pk]))
        self.assertContains(response, reverse(
            "exampleimage-update",
            args=[self.example_image.pk],
            urlconf="shastra_compedium.urls"))
        self.assertContains(response, reverse(
            "category-update",
            args=[self.example_image.position.category.pk],
            urlconf="shastra_compedium.urls"))
        self.assertContains(response, reverse(
            "exampleimage-update",
            urlconf="shastra_compedium.urls",
            args=[self.example_image.pk]))

    def test_changed_ids(self):
        login_as(self.user, self)
        response = self.client.get(
            "%s?changed_ids=[%s]&obj_type=ExampleImage" % (
                self.url,
                str(self.example_image.pk)))
        self.assertContains(
            response,
            "if ([%d].includes(row.id))" % self.example_image.image.pk)

    def test_list_empty(self):
        ex_url = reverse(
            "exampleimage-update",
            urlconf="shastra_compedium.urls",
            args=[self.example_image.pk])
        ExampleImage.objects.all().delete()
        Image.objects.filter(folder__name="PositionImageUploads").delete()
        response = self.client.get(self.url)
        self.assertNotContains(response, ex_url)
        self.assertNotContains(response, "'action':")

    def test_linked_detail(self):
        another_detail = PositionDetailFactory(
            position=self.example_image.position,
            usage="Posture Description")
        not_main_image = ExampleImageFactory(image=self.img1)
        not_main_image.details.add(another_detail)
        response = self.client.get(self.url)
        self.assertContains(response, another_detail.contents)
        self.assertContains(response, not_main_image.image.url)
        self.assertContains(
            response,
            '<i class="text-muted fas fa-times-circle fa-2x"></i>')

    def test_combo_only(self):
        combo = CombinationDetailFactory(
            positions=[self.example_image.position],
            usage="Meaning")
        self.combo_img = set_image(folder_name="PositionImageUploads")
        not_main_image = ExampleImageFactory(image=self.combo_img)
        not_main_image.combinations.add(combo)
        not_main_image.position = None
        not_main_image.save()
        response = self.client.get(self.url)
        self.assertContains(response, combo.contents)
        self.assertContains(response, not_main_image.image.url)
        self.assertContains(response, 'Combo Detail Only')

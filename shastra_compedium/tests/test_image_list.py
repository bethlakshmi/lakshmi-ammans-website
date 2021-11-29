from django.test import TestCase
from django.test import Client
from django.urls import reverse
from shastra_compedium.tests.factories import (
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
        login_as(self.user, self)

    def test_list_positions_basic(self):
        response = self.client.get(self.url)
        self.assertContains(response, self.example_image.position.name)
        self.assertContains(response, reverse(
            "exampleimage-update",
            urlconf="shastra_compedium.urls",
            args=[self.example_image.pk]))
        self.assertContains(response, self.img1.url)
        self.assertContains(
            response,
            '<i class="lakshmi-text-success far fa-check-square fa-3x"></i>')
        self.assertContains(
            response,
            '<a href="%s" class="nav-link active">Image List</a>' % (
                self.url),
            html=True)

    def test_list_image(self):
        self.img2 = set_image(folder_name="PositionImageUploads")
        response = self.client.get(self.url)
        self.assertContains(response, self.img2.url)
        self.assertContains(response, reverse(
            "exampleimage-add",
            urlconf="shastra_compedium.urls",
            args=[self.img2.pk]))

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
            '<i class="text-muted fas fa-times-circle fa-3x"></i>')
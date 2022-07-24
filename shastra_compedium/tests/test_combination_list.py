from django.test import TestCase
from django.test import Client
from django.urls import reverse
from shastra_compedium.tests.factories import (
    ExampleImageFactory,
    SubjectFactory,
    UserFactory
)
from shastra_compedium.tests.combo_context import CombinationContext
from shastra_compedium.models import CombinationDetail
from shastra_compedium.tests.functions import (
    login_as,
    set_image
)


class TestCombinationList(TestCase):
    view_name = "combo_list"

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.context = CombinationContext()
        self.combo = self.context.combo
        self.url = reverse(self.view_name, urlconf="shastra_compedium.urls")

    def test_list_basic_no_login(self):
        combo2 = CombinationContext(subject=self.combo.subject).combo
        response = self.client.get(self.url)
        self.assertContains(response, self.combo.positions.first().name)
        self.assertContains(response, self.combo.sources.first().title)
        self.assertContains(response, self.combo.contents)
        self.assertContains(response, reverse(
            "position-view",
            args=[self.combo.positions.first().pk],
            urlconf="shastra_compedium.urls"))
        self.assertNotContains(response, reverse(
            "combination-update",
            args=[self.combo.pk],
            urlconf="shastra_compedium.urls"))
        self.assertContains(response, self.combo.subject.name)
        self.assertContains(response, self.combo.contents)
        self.assertContains(response, combo2.contents)
        self.assertNotContains(response, reverse(
            "subject-update",
            args=[self.combo.subject.pk],
            urlconf="shastra_compedium.urls"))

    def test_list_w_login(self):
        self.context.set_images()
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, self.combo.contents)
        self.assertContains(response, reverse(
            "position-view",
            args=[self.combo.positions.first().pk],
            urlconf="shastra_compedium.urls"))
        self.assertContains(response, reverse(
            "combination-update",
            args=[self.combo.pk],
            urlconf="shastra_compedium.urls"))
        self.assertContains(response, self.context.img1.url)
        self.assertContains(response, self.context.img2.url)
        self.assertContains(response, reverse(
            "subject-update",
            args=[self.combo.subject.pk],
            urlconf="shastra_compedium.urls"))

    def test_list_w_main_image(self):
        spare_subject = SubjectFactory()
        self.img1 = set_image(folder_name="PositionImageUploads")
        self.example_image = ExampleImageFactory(
            image=self.img1,
            subject=spare_subject,
            general=True)
        response = self.client.get(self.url)
        self.assertContains(response, self.combo.contents)
        self.assertContains(response, self.img1.url)

    def test_list_empty(self):
        contents = self.combo.contents
        CombinationDetail.objects.all().delete()
        response = self.client.get(self.url)
        self.assertNotContains(response, contents)

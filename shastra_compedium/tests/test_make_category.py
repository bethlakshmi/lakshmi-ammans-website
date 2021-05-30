from django.test import TestCase
from django.urls import reverse
from django.test import Client
from shastra_compedium.tests.factories import (
    CategoryFactory,
    UserFactory,
)
from shastra_compedium.site_text import make_category_messages
from shastra_compedium.tests.functions import login_as
from shastra_compedium.models import Category


class TestMakeCategory(TestCase):
    '''Tests for category create & update'''

    add_name = 'category-add'
    update_name = 'category-update'

    def setUp(self):
        self.client = Client()
        self.object = CategoryFactory()
        self.create_url = reverse(self.add_name,
                                  urlconf='shastra_compedium.urls')
        self.edit_url = reverse(self.update_name,
                                args=[self.object.pk],
                                urlconf='shastra_compedium.urls')
        user = UserFactory()
        login_as(user, self)

    def category_data(self):
        return {'name': "New Name",
                'description': "Description"}

    def test_create_get(self):
        response = self.client.get(self.create_url, follow=True)
        self.assertContains(response, "Create Category")
        self.assertContains(response, make_category_messages['create_intro'])
        self.assertContains(response, "Name")

    def test_create_post(self):
        start = Category.objects.all().count()
        response = self.client.post(self.create_url,
                                    data=self.category_data(),
                                    follow=True)
        self.assertContains(
            response,
            make_category_messages['create_success'] % "New Name")
        self.assertEqual(start + 1, Category.objects.all().count())

    def test_create_error(self):
        data = self.category_data()
        data['name'] = ""
        response = self.client.post(self.create_url, data=data, follow=True)
        self.assertNotContains(
            response,
            make_category_messages['create_success'] % "New Name")
        self.assertContains(response, "This field is required.")
        self.assertContains(response, make_category_messages['create_intro'])

    def test_edit_get(self):
        response = self.client.get(self.edit_url)
        self.assertContains(response, "Update Category")
        self.assertContains(response, make_category_messages['edit_intro'])
        self.assertContains(response, "Name")

    def test_edit_post(self):
        start = Category.objects.all().count()
        response = self.client.post(self.edit_url,
                                    data=self.category_data(),
                                    follow=True)
        self.assertContains(
            response,
            make_category_messages['edit_success'] % "New Name")
        self.assertEqual(start, Category.objects.all().count())

    def test_edit_post_redirect(self):
        start = Category.objects.all().count()
        redirect_url = reverse("source_list", urlconf='shastra_compedium.urls')
        response = self.client.post(
            "%s?next=%s" % (self.edit_url, redirect_url),
            data=self.category_data(),
            follow=True)
        self.assertContains(
            response,
            make_category_messages['edit_success'] % "New Name")
        self.assertEqual(start, Category.objects.all().count())
        self.assertContains(
            response,
            '<a href="%s" class="nav-link active">Source List</a>' % (
                redirect_url),
            html=True)

    def test_edit_bad_data(self):
        data = self.category_data()
        data['name'] = ""
        response = self.client.post(self.edit_url, data=data, follow=True)
        self.assertNotContains(
            response,
            make_category_messages['edit_success'] % "New Name")
        self.assertContains(response, "This field is required.")
        self.assertContains(response, make_category_messages['edit_intro'])

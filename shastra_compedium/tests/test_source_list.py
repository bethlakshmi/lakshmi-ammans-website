from django.test import TestCase
from django.test import Client
from django.urls import reverse
from shastra_compedium.tests.factories import (
    CategoryDetailFactory,
    PositionDetailFactory,
    ShastraFactory,
    SourceFactory,
    UserFactory
)
from shastra_compedium.tests.functions import login_as


class TestSourceList(TestCase):
    view_name = "source_list"

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.source = SourceFactory()
        self.detail = PositionDetailFactory(usage="Meaning")
        self.detail.sources.add(self.source)
        self.detail.save()
        self.url = reverse(self.view_name, urlconf="shastra_compedium.urls")

    def test_list_sources_basic(self):
        from shastra_compedium.site_text import user_messages
        chapter = CategoryDetailFactory(category=self.detail.position.category)
        chapter.sources.add(self.source)
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response,
                            user_messages['SourceList']['description'])
        self.assertContains(response, self.source.title)
        self.assertContains(response, reverse(
            "source-update",
            urlconf="shastra_compedium.urls",
            args=[self.source.pk]))
        self.assertContains(
            response,
            '<a href="%s" class="nav-link active">Source List</a>' % (
                self.url),
            html=True)

    def test_list_sources_no_cat_detail(self):
        from shastra_compedium.site_text import user_messages
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response,
                            user_messages['SourceList']['description'])
        self.assertContains(response, self.source.title)
        self.assertContains(response, reverse(
            "source-update",
            urlconf="shastra_compedium.urls",
            args=[self.source.pk]))
        self.assertContains(
            response,
            '<a href="%s" class="nav-link active">Source List</a>' % (
                self.url),
            html=True)

    def test_list_categories_all_the_things(self):
        another_detail = PositionDetailFactory(
            usage="Posture Description")
        another_detail.sources.add(self.source)

        chapter = CategoryDetailFactory(category=self.detail.position.category)
        chapter.sources.add(self.source)
        another_shastra = ShastraFactory()

        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, "'id': %d" % self.source.pk)
        self.assertContains(response, "'shastra_id': %d" % another_shastra.pk)
        self.assertContains(response,
                            "'shastra_id': %d" % self.source.shastra.pk)
        self.assertContains(
            response,
            ("'title': '%s&nbsp;&nbsp;<a class=\"lakshmi-detail\" href=\"%s\"" +
             " title=\"Edit\"><i class=\"fas fa-edit\"></i></a>'") % (
                another_shastra.title,
                reverse("shastra-update",
                        urlconf="shastra_compedium.urls",
                        args=[another_shastra.pk])))
        self.assertContains(
            response,
            ("'title': '%s&nbsp;&nbsp;<a class=\"lakshmi-detail\" href=\"%s\"" +
             " title=\"Edit\"><i class=\"fas fa-edit\"></i></a>'") % (
                self.source.shastra.title,
                reverse("shastra-update",
                        urlconf="shastra_compedium.urls",
                        args=[self.source.shastra.pk])))

        self.assertContains(response,
                            "'publication': '%s'" % self.source.title)
        self.assertContains(response, "'publication': 'No Source Available'")
        self.assertContains(
            response,
            ('<a class="lakshmi-detail" href="%s" title="Edit"><i ' +
             'class="fas fa-edit"></i></a>') % (
             reverse("source-update",
                     urlconf="shastra_compedium.urls",
                     args=[self.source.pk])))
        print(response.content)
        self.assertContains(
            response,
            ('%s&nbsp;&nbsp;<a class="lakshmi-detail" href="%s?next=%s" ' +
             'title="Edit"><i class="fas fa-edit"></i></a>') % (
             another_detail.position.category.name,
             reverse("category-update",
                     urlconf="shastra_compedium.urls",
                     args=[another_detail.position.category.pk]),
             self.url))
        self.assertContains(
            response,
            ('%s&nbsp;&nbsp;<a class="lakshmi-detail" href="%s?next=%s" ' +
             'title="Edit"><i class="fas fa-edit"></i></a>') % (
             self.detail.position.category.name,
             reverse("category-update",
                     urlconf="shastra_compedium.urls",
                     args=[self.detail.position.category.pk]),
             self.url))
        self.assertContains(
            response,
            ('<a class="lakshmi-detail" href="%s" title="Edit Chapter"><i ' +
             'class="fas fa-edit"></i></a>') % reverse(
             "categorydetail-update",
             urlconf="shastra_compedium.urls",
             args=[chapter.pk]))

    def test_list_empty(self):
        from shastra_compedium.site_text import user_messages
        ex_url = reverse(
            "position-update",
            urlconf="shastra_compedium.urls",
            args=[self.detail.pk])
        self.detail.delete()
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response,
                            user_messages['SourceList']['description'])
        self.assertNotContains(response, ex_url)
        self.assertContains(response, "'action':")

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

    def test_list_categories_changed_ids(self):
        another_detail = PositionDetailFactory(
            usage="Posture Description")
        another_detail.sources.add(self.source)

        chapter = CategoryDetailFactory(category=self.detail.position.category)
        chapter.sources.add(self.source)
        another_shastra = ShastraFactory()

        login_as(self.user, self)
        response = self.client.get("%s?changed_ids=%s&obj_type=Source" % (
            self.url,
            str([self.source.pk])))
        self.assertContains(response, "[%d].includes(row.id)" % self.source.pk)

    def test_list_categories_changed_shastra_ids(self):
        another_detail = PositionDetailFactory(
            usage="Posture Description")
        another_detail.sources.add(self.source)

        chapter = CategoryDetailFactory(category=self.detail.position.category)
        chapter.sources.add(self.source)
        another_shastra = ShastraFactory()

        login_as(self.user, self)
        response = self.client.get("%s?changed_ids=%s&obj_type=Shastra" % (
            self.url,
            str([self.source.shastra.pk])))
        self.assertContains(
            response,
            "[%d].includes(row.shastra_id)" % self.source.shastra.pk)

    def test_list_categories_changed_category_ids(self):
        another_detail = PositionDetailFactory(
            usage="Posture Description")
        another_detail.sources.add(self.source)

        chapter = CategoryDetailFactory(category=self.detail.position.category)
        chapter.sources.add(self.source)
        another_shastra = ShastraFactory()

        login_as(self.user, self)
        response = self.client.get("%s?changed_ids=%s&obj_type=Category" % (
            self.url,
            str([self.detail.position.category.pk])))
        self.assertContains(
            response,
            "[].includes(row.id)")

    def test_list_categories_changed_categorydetail(self):
        another_detail = PositionDetailFactory(
            usage="Posture Description")
        another_detail.sources.add(self.source)

        chapter = CategoryDetailFactory(
            category=self.detail.position.category,
            chapter=10,
            verse_start=1,
            verse_end=100)
        chapter.sources.add(self.source)
        another_shastra = ShastraFactory()

        login_as(self.user, self)
        response = self.client.get(
            "%s?changed_ids=%s&obj_type=CategoryDetail" % (
                self.url,
                str([chapter.pk])))
        self.assertContains(
            response,
            ('<td class="lakshmi-table-success">10:1-100<a class="lakshmi-' +
             'detail" href="%s" title="Edit Chapter"><i class="fas fa-edit">' +
             '</i></a></td>') % reverse(
             "categorydetail-update",
             urlconf="shastra_compedium.urls",
             args=[chapter.pk]))

    def test_list_category_detail_variations(self):
        chapter = CategoryDetailFactory(
            category=self.detail.position.category,
            chapter=10,
            verse_start=1,
            verse_end=100)
        chapter.sources.add(self.source)
        chapter2 = CategoryDetailFactory(verse_end=50)
        chapter2.sources.add(self.source)
        chapter_more = CategoryDetailFactory(
            category=self.detail.position.category,
            chapter=10,
            verse_start=101,
            verse_end=200)
        chapter_more.sources.add(self.source)

        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(
            response,
            ('<a class="lakshmi-detail" href="%s" title="Edit Chapter"><i ' +
             'class="fas fa-edit"></i></a>') % reverse(
             "categorydetail-update",
             urlconf="shastra_compedium.urls",
             args=[chapter.pk]))
        self.assertContains(
            response,
            ('<a class="lakshmi-detail" href="%s" title="Edit Chapter"><i ' +
             'class="fas fa-edit"></i></a>') % reverse(
             "categorydetail-update",
             urlconf="shastra_compedium.urls",
             args=[chapter2.pk]))
        self.assertContains(
            response,
            ('<a class="lakshmi-detail" href="%s" title="Edit Chapter"><i ' +
             'class="fas fa-edit"></i></a>') % reverse(
             "categorydetail-update",
             urlconf="shastra_compedium.urls",
             args=[chapter_more.pk]))

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

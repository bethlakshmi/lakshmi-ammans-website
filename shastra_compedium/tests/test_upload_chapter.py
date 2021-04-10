from django.test import TestCase
from django.urls import reverse
from django.test import Client
from shastra_compedium.tests.factories import (
    CategoryFactory,
    PositionFactory,
    SourceFactory,
    UserFactory,
)
from shastra_compedium.site_text import user_messages
from shastra_compedium.tests.functions import login_as
from shastra_compedium.models import (
    CategoryDetail,
    PositionDetail,
)


class TestUploadChapter(TestCase):
    '''Tests for source create & update'''

    add_name = 'chapter-add'

    def setUp(self):
        self.client = Client()
        self.create_url = reverse(self.add_name,
                                  urlconf='shastra_compedium.urls')
        user = UserFactory()
        login_as(user, self)

    def chapter_data(self):
        self.category = CategoryFactory()
        self.source = SourceFactory()
        return {'sources': [self.source.pk],
                'category': self.category.pk,
                'usage': "test",
                'chapter': 1,
                'contents': "Contents",
                'position_text': "Position text",
                'verse_start': 10,
                'verse_end': 20,
                'step': 0,
                'next': True}

    def position_data(self):
        self.source = SourceFactory()
        self.position = PositionFactory()
        return {'0-sources': [self.source.pk],
                '0-usage': "Meaning",
                '0-position': self.position.pk,
                '0-chapter': 1,
                '0-verse_start': 10,
                '0-verse_end': 20,
                '0-posture': "Posture text",
                '0-contents': "Meaning text",
                'step': 1,
                'num_rows': 1,
                'finish': True}

    def test_create_get(self):
        response = self.client.get(self.create_url, follow=True)
        self.assertContains(response, "Upload Chapter")
        self.assertContains(
            response,
            user_messages['CHAPTER_BASICS_INTRO']['description'])
        self.assertContains(response, "Sources")

    def test_create_post_basics_success(self):
        start = CategoryDetail.objects.all().count()
        data = self.chapter_data()
        data['position_text'] = "3-4 Description One(Uses)Meaning One|||" + \
            "5 Description Two(Uses)Meaning Two"
        response = self.client.post(self.create_url,
                                    data=data,
                                    follow=True)
        self.assertEqual(start + 1, CategoryDetail.objects.all().count())
        self.assertContains(
            response,
            user_messages['CHAPTER_DETAIL_INTRO']['description'])
        self.assertContains(
            response,
            ('<input type="hidden" name="0-sources" value="%d" ' +
             'id="id_0-sources_0">') % self.source.pk,
            html=True)
        self.assertContains(
            response,
            '<textarea name="0-posture" cols="40" rows="10" class="' +
            'admin-tiny-mce" id="id_0-posture">\nDescription One</textarea>',
            html=True)
        self.assertContains(
            response,
            '<textarea name="0-contents" cols="40" rows="10" class="' +
            'admin-tiny-mce" id="id_0-contents">\nMeaning One</textarea>',
            html=True)
        self.assertContains(
            response,
            '<textarea name="1-posture" cols="40" rows="10" class="' +
            'admin-tiny-mce" id="id_1-posture">\nDescription Two</textarea>',
            html=True)
        self.assertContains(
            response,
            '<textarea name="1-contents" cols="40" rows="10" class="' +
            'admin-tiny-mce" id="id_1-contents">\nMeaning Two</textarea>',
            html=True)
        self.assertContains(
            response,
            '<input type="number" name="0-chapter" value="1" ' +
            'style="width: 50px" id="id_0-chapter">',
            html=True)
        self.assertContains(
            response,
            '<input type="number" name="0-verse_start" value="3" ' +
            'style="width: 50px" id="id_0-verse_start">',
            html=True)
        self.assertContains(
            response,
            '<input type="number" name="0-verse_end" value="4" ' +
            'style="width: 50px" id="id_0-verse_end">',
            html=True)
        self.assertContains(
            response,
            '<input type="number" name="1-verse_start" value="5" ' +
            'style="width: 50px" id="id_1-verse_start">',
            html=True)
        self.assertContains(
            response,
            reverse('position-add',
                    urlconf='shastra_compedium.urls',
                    args=[0, self.category.pk]))

    def test_create_post_basics_finish(self):
        start = CategoryDetail.objects.all().count()
        data = self.chapter_data()
        del data['next']
        data['finish'] = True
        response = self.client.post(self.create_url,
                                    data=data,
                                    follow=True)
        self.assertEqual(start + 1, CategoryDetail.objects.all().count())
        self.assertNotContains(
            response,
            user_messages['CHAPTER_DETAIL_INTRO']['description'])
        self.assertContains(
            response,
            ("Uploaded chapter details - Detail for Category %s, from " +
             "Source(s): %s") % (self.category.name, self.source))

    def test_create_error(self):
        data = self.chapter_data()
        data['category'] = self.category.pk + 1
        response = self.client.post(self.create_url, data=data, follow=True)
        self.assertNotContains(
            response,
            "Upload Chapter - Edit Detail Entries")
        self.assertContains(
            response,
            "Select a valid choice. That choice is not one of the " +
            "available choices.")
        self.assertContains(
            response,
            user_messages['CHAPTER_BASICS_INTRO']['description'])

    def test_create_post_positions_success(self):
        start = PositionDetail.objects.all().count()
        response = self.client.post(self.create_url,
                                    data=self.position_data(),
                                    follow=True)
        self.assertRedirects(response, reverse(
            "position_list",
            urlconf='shastra_compedium.urls'))
        self.assertContains(response, "Uploaded 2 position details.")
        self.assertEqual(start + 2, PositionDetail.objects.all().count())

    def test_create_post_positions_format_fail(self):
        data = self.position_data()
        del data['num_rows']
        response = self.client.post(self.create_url,
                                    data=data,
                                    follow=True)
        self.assertRedirects(response, reverse(
            "position_list",
            urlconf='shastra_compedium.urls'))
        self.assertContains(
            response,
            user_messages['NO_FORM_ERROR']['description'])

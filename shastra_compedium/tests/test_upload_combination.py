from django.test import TestCase
from django.urls import reverse
from django.test import Client
from shastra_compedium.tests.factories import (
    CategoryFactory,
    CategoryDetailFactory,
    PositionFactory,
    SourceFactory,
    UserFactory,
)
from shastra_compedium.site_text import user_messages
from shastra_compedium.tests.functions import login_as
from shastra_compedium.models import (
    CategoryDetail,
    CombinationDetail,
)


class TestUploadChapter(TestCase):
    '''Tests for source create & update'''

    add_name = 'combinations-add'

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
                '0-positions': [self.position.pk],
                '0-chapter': 1,
                '0-verse_start': 10,
                '0-verse_end': 20,
                '0-contents': "Posture text",
                'step': 1,
                'num_rows': 1,
                'finish': True}

    def test_create_get(self):
        response = self.client.get(self.create_url, follow=True)
        self.assertContains(response, 'Upload Combinations')
        self.assertContains(
            response,
            user_messages['COMBINATION_BASICS_INTRO']['description'])
        self.assertContains(response, "Sources")

    def test_add_more_get(self):
        chapter = CategoryDetailFactory()
        self.create_url = reverse('combinations-additional',
                                  urlconf='shastra_compedium.urls',
                                  args=[chapter.pk])
        response = self.client.get(self.create_url, follow=True)
        self.assertContains(response, "Upload Combinations")
        self.assertContains(
            response,
            user_messages['COMBINATION_BASICS_INTRO']['description'])
        self.assertContains(response, "Sources")
        self.assertContains(response, chapter.contents)

    def test_create_post_basics_success(self):
        start = CategoryDetail.objects.all().count()
        data = self.chapter_data()
        data['position_text'] = "3-4 Combo One|||5 Combo Two"
        response = self.client.post(self.create_url,
                                    data=data,
                                    follow=True)
        self.assertEqual(start + 1, CategoryDetail.objects.all().count())
        self.assertContains(
            response,
            user_messages['COMBINATION_DETAIL_INTRO']['description'])
        self.assertContains(
            response,
            ('<input type="hidden" name="0-sources" value="%d" ' +
             'id="id_0-sources_0">') % self.source.pk,
            html=True)
        self.assertContains(
            response,
            '<textarea name="0-contents" cols="40" rows="10" class="' +
            'admin-tiny-mce" id="id_0-contents">\nCombo One</textarea>',
            html=True)
        self.assertContains(
            response,
            '<textarea name="1-contents" cols="40" rows="10" class="' +
            'admin-tiny-mce" id="id_1-contents">\nCombo Two</textarea>',
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

    def test_create_post_positions_success(self):
        start = CombinationDetail.objects.all().count()
        response = self.client.post(self.create_url,
                                    data=self.position_data(),
                                    follow=True)
        print(response.content)
        last_pk = CombinationDetail.objects.latest('pk').pk
        self.assertRedirects(
            response,
            "%s?changed_ids=%s&obj_type=CombinationDetail" % (
                reverse("combo_list", urlconf='shastra_compedium.urls'),
                str([last_pk])))
        self.assertContains(response, "Uploaded 1 details.")
        self.assertEqual(start + 1, CombinationDetail.objects.all().count())

    def test_create_post_positions_to_existing_chapter(self):
        chapter = CategoryDetailFactory()
        self.create_url = reverse('combinations-additional',
                                  urlconf='shastra_compedium.urls',
                                  args=[chapter.pk])
        start = CombinationDetail.objects.all().count()
        response = self.client.post(self.create_url,
                                    data=self.position_data(),
                                    follow=True)
        print(response.content)
        last_pk = CombinationDetail.objects.latest('pk').pk
        self.assertRedirects(
            response,
            "%s?changed_ids=%s&obj_type=CombinationDetail" % (
                reverse("combo_list", urlconf='shastra_compedium.urls'),
                str([last_pk])))
        self.assertContains(response, "Uploaded 1 details.")
        self.assertEqual(start + 1, CombinationDetail.objects.all().count())

    def test_create_post_positions_success_without_upload(self):
        data = self.position_data()
        data['0-positions'] = []
        data['1-sources'] = [self.source.pk]
        data['1-usage'] = "Meaning",
        data['1-positions'] = [self.position.pk],
        data['1-chapter'] = 1
        data['1-verse_start'] = 10
        data['1-verse_end'] = 20
        response = self.client.post(self.create_url,
                                    data=data,
                                    follow=True)
        self.assertRedirects(response, reverse(
            "combo_list",
            urlconf='shastra_compedium.urls'))
        self.assertContains(response, "Uploaded 0 details.")

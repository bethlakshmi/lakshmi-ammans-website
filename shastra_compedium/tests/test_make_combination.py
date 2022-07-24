from django.test import TestCase
from django.urls import reverse
from django.test import Client
from shastra_compedium.tests.factories import (
    CombinationDetailFactory,
    PositionFactory,
    SourceFactory,
    SubjectFactory,
    UserFactory,
)
from shastra_compedium.site_text import make_combination_messages
from shastra_compedium.tests.functions import login_as
from shastra_compedium.models import CombinationDetail


class TestMakeCombination(TestCase):
    '''Tests for position create & update'''

    update_name = 'combination-update'

    def setUp(self):
        self.client = Client()
        self.object = CombinationDetailFactory()
        self.edit_url = reverse(self.update_name,
                                args=[self.object.pk],
                                urlconf='shastra_compedium.urls')
        user = UserFactory()
        login_as(user, self)

    def combination_data(self):
        self.pos1 = PositionFactory()
        self.pos2 = PositionFactory()
        source = SourceFactory()
        self.subject = SubjectFactory()
        return {'positions': [self.pos1.pk, self.pos2.pk],
                'chapter': 2,
                'verse_start': 3,
                'verse_end': 4,
                'usage': 'Deep Meaning',
                'subject': self.subject.pk,
                'sources': [source.pk],
                'contents': '<p>Do stuff with other stuff</p>',
                }

    def test_edit_get(self):
        response = self.client.get(self.edit_url)
        self.assertContains(response, "Update Combination")
        self.assertContains(response, make_combination_messages['edit_intro'])
        self.assertContains(response, "Positions")

    def test_edit_post(self):
        start = CombinationDetail.objects.all().count()
        response = self.client.post(self.edit_url,
                                    data=self.combination_data(),
                                    follow=True)
        self.assertContains(
            response,
            make_combination_messages['edit_success'] % (
                self.subject.name + " - 2:3-4 - Do stuff with other stuff..."))
        self.assertEqual(start, CombinationDetail.objects.all().count())

    def test_edit_bad_data(self):
        data = self.combination_data()
        data['positions'] = []
        response = self.client.post(self.edit_url, data=data, follow=True)
        self.assertNotContains(
            response,
            make_combination_messages['edit_success'] % (
                "2:3-4 - Do stuff with other stuff..."))
        self.assertContains(response, "This field is required.")
        self.assertContains(response, make_combination_messages['edit_intro'])

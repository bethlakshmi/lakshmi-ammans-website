from django.test import TestCase
from django.urls import reverse
from django.test import Client
from shastra_compedium.tests.factories import (
    CategoryFactory,
    SourceFactory,
    UserFactory,
)
from shastra_compedium.site_text import user_messages
from shastra_compedium.tests.functions import login_as
from shastra_compedium.models import CategoryDetail


class TestGenericWizard(TestCase):
    '''Tests that are focused on create wizard.  It uses chapter-add but
    focuses on parent test cases'''

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


    def test_no_step(self):
        data = self.chapter_data()
        del data['step']
        response = self.client.post(self.create_url,
                                    data=data,
                                    follow=True)
        self.assertContains(
            response,
            user_messages['STEP_ERROR']['description'])

    def test_bad_button(self):
        data = self.chapter_data()
        del data['next']
        response = self.client.post(self.create_url, data=data, follow=True)
        self.assertContains(
            response,
            user_messages['BUTTON_CLICK_UNKNOWN']['description'])

    def test_cancel(self):
        data = self.chapter_data()
        del data['next']
        data['cancel'] = True
        response = self.client.post(self.create_url, data=data, follow=True)
        self.assertRedirects(response, reverse(
            "position_list",
             urlconf='shastra_compedium.urls'))
        # part of the success message - no positions are posted
        self.assertNotContains(response, "position details.")

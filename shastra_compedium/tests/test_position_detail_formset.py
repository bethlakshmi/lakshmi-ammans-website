from django.test import TestCase
from django.urls import reverse
from django.test import Client
from shastra_compedium.tests.factories import (
    CategoryFactory,
    PositionDetailFactory,
    SourceFactory,
    UserFactory,
)
from shastra_compedium.site_text import edit_post_detail_messages
from shastra_compedium.forms.default_form_text import position_detail_help
from shastra_compedium.tests.functions import (
    assert_option_state,
    login_as,
)
from shastra_compedium.models import (
    CategoryDetail,
    PositionDetail,
)


class TestPositionDetailFormset(TestCase):
    '''Tests for source create & update'''

    view_name = 'position-detail-update'

    def setUp(self):
        self.client = Client()
        user = UserFactory()
        login_as(user, self)

    def test_get_by_position_w_next(self):
        detail = PositionDetailFactory()
        pos_list = reverse('position_list', urlconf='shastra_compedium.urls')
        response = self.client.get("%s?next=%s" % (
            reverse(self.view_name,
                    urlconf='shastra_compedium.urls',
                    args=[detail.position.id]),
            pos_list),
            follow=True)
        self.assertContains(response, "Edit Position Details")
        self.assertContains(
            response,
            edit_post_detail_messages['intro'])
        self.assertContains(response, detail.contents)
        self.assertContains(response, pos_list)

    def test_get_by_source_category(self):
        detail = PositionDetailFactory()
        source = SourceFactory()
        detail.sources.add(source)
        response = self.client.get(
            reverse(self.view_name,
                    urlconf='shastra_compedium.urls',
                    args=[source.id, detail.position.category.id]),
            follow=True)
        self.assertContains(response, "Edit Position Details")
        self.assertContains(
            response,
            edit_post_detail_messages['intro'])
        self.assertContains(response, detail.contents)
        self.assertContains(
            response,
            reverse('source_list', urlconf="shastra_compedium.urls"))

    def test_get_by_source_no_category(self):
        detail = PositionDetailFactory(position__category=None)
        source = SourceFactory()
        detail.sources.add(source)
        response = self.client.get(reverse(self.view_name,
                                           urlconf='shastra_compedium.urls',
                                           args=[source.id, '']),
                                   follow=True)
        self.assertContains(response, "Edit Position Details")
        self.assertContains(
            response,
            edit_post_detail_messages['intro'])
        self.assertContains(response, detail.contents)

    def test_get_w_description(self):
        detail = PositionDetailFactory()
        source = SourceFactory()
        detail.description = PositionDetailFactory(position=detail.position,
                                                   usage="Posture Description")
        detail.sources.add(source)
        detail.description.sources.add(source)
        detail.save()
        response = self.client.get(reverse(self.view_name,
                                           urlconf='shastra_compedium.urls',
                                           args=[detail.position.id]),
                                   follow=True)
        assert_option_state(self,
                            response,
                            detail.description.pk,
                            "%s - %s - %s..." % (
                                detail.description.position.name,
                                detail.description.verses(),
                                detail.description.contents[3:28]),
                            True)

    def test_get_w_dependancy(self):
        detail = PositionDetailFactory()
        source = SourceFactory()
        dependancy = PositionDetailFactory(usage="Posture Description")
        detail.sources.add(source)
        dependancy.sources.add(source)
        detail.dependencies.add(dependancy)
        response = self.client.get(reverse(self.view_name,
                                           urlconf='shastra_compedium.urls',
                                           args=[detail.position.id]),
                                   follow=True)
        assert_option_state(self,
                            response,
                            dependancy.pk,
                            "%s - %s - %s..." % (
                                dependancy.position.name,
                                dependancy.verses(),
                                dependancy.contents[3:28]),
                            True)

    def test_post_by_source(self):
        detail = PositionDetailFactory()
        detail2 = PositionDetailFactory(position=detail.position)
        detail3 = PositionDetailFactory(
            position__category=detail.position.category)
        source = SourceFactory()
        detail.sources.add(source)
        detail2.sources.add(source)
        detail3.sources.add(source)
        response = self.client.post(
            reverse(self.view_name,
                    urlconf='shastra_compedium.urls',
                    args=[source.id, detail.position.category.id]),
            data={'form-0-sources': [source.pk],
                  'form-0-usage': "Meaning",
                  'form-0-position': detail.position.pk,
                  'form-0-chapter': 1,
                  'form-0-verse_start': 10,
                  'form-0-verse_end': 20,
                  'form-0-contents': "Meaning text",
                  'form-0-id': detail.id,
                  'form-1-sources': [source.pk],
                  'form-1-usage': "Posture Description",
                  'form-1-position': detail2.position.pk,
                  'form-1-chapter': 1,
                  'form-1-verse_start': 10,
                  'form-1-verse_end': 20,
                  'form-1-contents': "Meaning text",
                  'form-1-id': detail3.id,
                  'form-2-sources': [source.pk],
                  'form-2-usage': "Meaning",
                  'form-2-position': detail3.position.pk,
                  'form-2-chapter': 1,
                  'form-2-verse_start': 20,
                  'form-2-verse_end': 30,
                  'form-2-contents': "Meaning text",
                  'form-2-id': detail3.id,
                  'form-TOTAL_FORMS': 3,
                  'form-INITIAL_FORMS': 3,
                  'form-MIN_NUM_FORMS': 0,
                  'form-MAX_NUM_FORMS': 1000,
                  'submit': True},
            follow=True)
        self.assertContains(response, "List of Sources")
        self.assertContains(
            response,
            "%s, %s position details were updated." % (
                detail3.position.name,
                detail.position.name))
        self.assertRedirects(
            response,
            "%s?changed_ids=[%d]&obj_type=Source" % (
                reverse('source_list', urlconf='shastra_compedium.urls'),
                source.id))

    def test_post_w_next(self):
        detail = PositionDetailFactory()
        source = SourceFactory()
        pos_list = reverse('position_list', urlconf='shastra_compedium.urls')
        response = self.client.post(
            "%s?next=%s" % (reverse(self.view_name,
                                    urlconf='shastra_compedium.urls',
                                    args=[detail.position.id]), pos_list),
            data={'form-0-sources': [source.pk],
                  'form-0-usage': "Meaning",
                  'form-0-position': detail.position.pk,
                  'form-0-chapter': 1,
                  'form-0-verse_start': 10,
                  'form-0-verse_end': 20,
                  'form-0-contents': "Meaning text",
                  'form-0-id': detail.id,
                  'form-TOTAL_FORMS': 1,
                  'form-INITIAL_FORMS': 1,
                  'form-MIN_NUM_FORMS': 0,
                  'form-MAX_NUM_FORMS': 1000,
                  'submit': True},
            follow=True)
        self.assertRedirects(
            response,
            "%s?changed_ids=[%d]&obj_type=Position" % (pos_list,
                                                       detail.position.id))
        self.assertContains(response, "List of Positions")
        self.assertContains(
            response,
            "%s position details were updated." % detail.position.name)

    def test_post_w_source_description_conflict(self):
        detail = PositionDetailFactory()
        source = SourceFactory()
        pos_list = reverse('position_list', urlconf='shastra_compedium.urls')
        description = PositionDetailFactory(
            position=detail.position,
            usage="Posture Description")
        response = self.client.post(
            "%s?next=%s" % (reverse(self.view_name,
                                    urlconf='shastra_compedium.urls',
                                    args=[detail.position.id]), pos_list),
            data={'form-0-sources': [source.pk],
                  'form-0-usage': "Meaning",
                  'form-0-position': detail.position.pk,
                  'form-0-chapter': 1,
                  'form-0-verse_start': 10,
                  'form-0-verse_end': 20,
                  'form-0-contents': "Meaning text",
                  'form-0-id': detail.id,
                  'form-0-description': description.pk,
                  'form-TOTAL_FORMS': 1,
                  'form-INITIAL_FORMS': 1,
                  'form-MIN_NUM_FORMS': 0,
                  'form-MAX_NUM_FORMS': 1000,
                  'submit': True},
            follow=True)
        self.assertContains(response, "Edit Position Details")
        self.assertContains(
            response,
            position_detail_help['same_source'])

    def test_post_w_source_dependancy_conflict(self):
        detail = PositionDetailFactory()
        source = SourceFactory()
        pos_list = reverse('position_list', urlconf='shastra_compedium.urls')
        dependancy = PositionDetailFactory(usage="Posture Description")
        response = self.client.post(
            "%s?next=%s" % (reverse(self.view_name,
                                    urlconf='shastra_compedium.urls',
                                    args=[detail.position.id]), pos_list),
            data={'form-0-sources': [source.pk],
                  'form-0-usage': "Meaning",
                  'form-0-position': detail.position.pk,
                  'form-0-chapter': 1,
                  'form-0-verse_start': 10,
                  'form-0-verse_end': 20,
                  'form-0-contents': "Meaning text",
                  'form-0-id': detail.id,
                  'form-0-dependencies': [dependancy.pk],
                  'form-TOTAL_FORMS': 1,
                  'form-INITIAL_FORMS': 1,
                  'form-MIN_NUM_FORMS': 0,
                  'form-MAX_NUM_FORMS': 1000,
                  'submit': True},
            follow=True)
        self.assertContains(response, "Edit Position Details")
        self.assertContains(
            response,
            position_detail_help['same_source2'] % str(dependancy))

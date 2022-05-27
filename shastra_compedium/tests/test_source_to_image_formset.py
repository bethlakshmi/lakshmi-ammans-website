from django.test import TestCase
from django.urls import reverse
from django.test import Client
from shastra_compedium.tests.factories import (
    CategoryFactory,
    ExampleImageFactory,
    PositionDetailFactory,
    SourceFactory,
    UserFactory,
)
from shastra_compedium.site_text import edit_pos_image_link_messages
from shastra_compedium.tests.functions import (
    assert_option_state,
    login_as,
    set_image,
)
from shastra_compedium.models import (
    CategoryDetail,
    PositionDetail,
)


class TestSourceToImageFormset(TestCase):
    '''Tests for source create & update'''

    view_name = 'position-detail-image-update'

    def setUp(self):
        self.client = Client()
        user = UserFactory()
        login_as(user, self)
        self.return_list = reverse('source_list',
                                   urlconf='shastra_compedium.urls')
        self.detail = PositionDetailFactory()
        self.source = SourceFactory()
        self.detail.sources.add(self.source)
        img1 = set_image()
        self.example_image = ExampleImageFactory(image=img1,
                                                 position=self.detail.position)

    def test_get_by_source_category(self):
        response = self.client.get(
            reverse(self.view_name,
                    urlconf='shastra_compedium.urls',
                    args=[self.source.id, self.detail.position.category.id]),
            follow=True)
        self.assertContains(response, "Edit Image to Position Assignments")
        self.assertContains(
            response,
            edit_pos_image_link_messages['intro'])
        self.assertContains(response, self.detail.contents)
        self.assertContains(
            response,
            reverse('source_list', urlconf="shastra_compedium.urls"))
        self.assertContains(response, self.return_list)
        self.assertContains(response,
                            self.example_image.image.original_filename)

    def test_get_w_dependancy(self):
        dependancy = PositionDetailFactory(usage="Posture Description")
        dependancy.sources.add(self.source)
        self.example_image.details.add(self.detail)
        self.detail.dependencies.add(dependancy)
        img1 = set_image()
        d_example_image = ExampleImageFactory(
            image=img1,
            position=dependancy.position)
        d_example_image.details.add(dependancy)
        response = self.client.get(reverse(
            self.view_name,
            urlconf='shastra_compedium.urls',
            args=[self.source.id,
                  self.detail.position.category.id]), follow=True)
        assert_option_state(self,
                            response,
                            dependancy.pk,
                            "%s - %s - %s..." % (
                                dependancy.position.name,
                                dependancy.verses(),
                                dependancy.contents[3:28]),
                            True)
        self.assertContains(response,
                            self.example_image.image.original_filename)
        self.assertContains(response,
                            d_example_image.image.original_filename)
        self.assertContains(
            response,
            ('<input type="checkbox" name="form-0-exampleimage_set" ' +
             'value="%s" class="nobullet" id="id_form-0-exampleimage_set_0"' +
             ' checked>') % (self.example_image.pk),
            html=True)

    def test_post_by_source(self):
        detail2 = PositionDetailFactory(position=self.detail.position)
        detail3 = PositionDetailFactory(
            position__category=self.detail.position.category)
        detail2.sources.add(self.source)
        detail3.sources.add(self.source)
        dependancy = PositionDetailFactory(usage="Posture Description")
        dependancy.sources.add(self.source)
        self.example_image.details.add(self.detail)
        self.detail.dependencies.add(dependancy)
        img1 = set_image()
        d3_example_image = ExampleImageFactory(
            image=img1,
            position=detail3.position)
        response = self.client.post(
            reverse(self.view_name,
                    urlconf='shastra_compedium.urls',
                    args=[self.source.id, self.detail.position.category.id]),
            data={'form-0-id': self.detail.id,
                  'form-0-exampleimage_set': [self.example_image.pk],
                  'form-0-dependencies': [],
                  'form-1-id': detail2.id,
                  'form-1-exampleimage_set': [],
                  'form-1-dependencies': [dependancy.pk],
                  'form-2-id': detail3.id,
                  'form-2-exampleimage_set': [d3_example_image.pk],
                  'form-2-dependencies': [dependancy.pk],
                  'form-TOTAL_FORMS': 3,
                  'form-INITIAL_FORMS': 3,
                  'form-MIN_NUM_FORMS': 0,
                  'form-MAX_NUM_FORMS': 1000,
                  'submit': True},
            follow=True)
        self.assertContains(response, "List of Sources")
        self.assertContains(
            response,
            "%s, %s position detail images were updated." % (
                detail3.position.name,
                self.detail.position.name))
        self.assertRedirects(
            response,
            "%s?changed_ids=[%d]&obj_type=Source" % (
                reverse('source_list', urlconf='shastra_compedium.urls'),
                self.source.id))
        test_detail3 = PositionDetail.objects.get(id=detail3.id)
        self.assertEqual(test_detail3.exampleimage_set.first(),
                         d3_example_image)
        self.assertEqual(test_detail3.dependencies.first(),
                         dependancy)

    def test_post_bad_image(self):
        detail3 = PositionDetailFactory(
            position__category=self.detail.position.category)
        detail3.sources.add(self.source)
        dependancy = PositionDetailFactory(usage="Posture Description")
        dependancy.sources.add(self.source)
        self.example_image.details.add(self.detail)
        self.detail.dependencies.add(dependancy)
        response = self.client.post(
            reverse(self.view_name,
                    urlconf='shastra_compedium.urls',
                    args=[self.source.id, self.detail.position.category.id]),
            data={'form-0-id': self.detail.id,
                  'form-0-exampleimage_set': [self.example_image.pk],
                  'form-0-dependencies': [],
                  'form-1-id': detail3.id,
                  'form-1-exampleimage_set': [self.example_image.pk],
                  'form-1-dependencies': [dependancy.pk],
                  'form-TOTAL_FORMS': 2,
                  'form-INITIAL_FORMS': 2,
                  'form-MIN_NUM_FORMS': 0,
                  'form-MAX_NUM_FORMS': 1000,
                  'submit': True},
            follow=True)
        self.assertNotContains(response, "List of Sources")
        self.assertContains(
            response,
            "%d is not one of the available choices." % self.example_image.pk)

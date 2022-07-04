from django.test import (
    Client,
    TestCase
)
from django.contrib.auth.models import User
from shastra_compedium.tests.factories import (
    CategoryDetailFactory,
    CombinationDetailFactory,
    ExampleImageFactory,
    PerformerFactory,
    PositionDetailFactory,
    SourceFactory,
    UserFactory,
)
from shastra_compedium.tests.functions import (
    login_as,
    set_image
)
from datetime import (
    date,
    timedelta,
)
from django.contrib.admin.sites import AdminSite


class AdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        password = 'mypassword'
        self.privileged_user = User.objects.create_superuser(
            'myuser', 'myemail@test.com', password)
        self.client.login(
            username=self.privileged_user.username,
            password=password)

    def test_get_shastra(self):
        obj = SourceFactory()
        response = self.client.get('/admin/shastra_compedium/shastra/',
                                   follow=True)
        self.assertContains(response, obj.shastra.title)
        self.assertContains(response, '<td class="field-source_count">1</td>')

    def test_get_source(self):
        obj = SourceFactory(shastra__author="Author")
        response = self.client.get('/admin/shastra_compedium/source/',
                                   follow=True)
        self.assertContains(response, obj.shastra.title)
        self.assertContains(response, obj.shastra.author)
        self.assertContains(response, obj.shastra.min_age)
        self.assertContains(response, obj.shastra.max_age)

    def test_get_categorydetail(self):
        obj = CategoryDetailFactory()
        obj.sources.add(SourceFactory())
        response = self.client.get('/admin/shastra_compedium/categorydetail/',
                                   follow=True)
        self.assertContains(response, obj.category.name)
        self.assertContains(response, '<td class="field-source_count">1</td>')

    def test_get_positiondetail(self):
        obj = PositionDetailFactory()
        obj.sources.add(SourceFactory())
        response = self.client.get('/admin/shastra_compedium/positiondetail/',
                                   follow=True)
        self.assertContains(response, obj.position.name)
        self.assertContains(response, '<td class="field-source_count">1</td>')

    def test_get_position(self):
        obj = PositionDetailFactory()
        obj.sources.add(SourceFactory())
        response = self.client.get('/admin/shastra_compedium/position/',
                                   follow=True)
        self.assertContains(response, obj.position.name)
        self.assertContains(response, '<td class="field-detail_count">1</td>')
        self.assertContains(response,
                            '<td class="field-example_image_count">0</td>')
        self.assertContains(response,
                            '<td class="field-example_video_count">0</td>')

    def test_get_performer(self):
        obj = PerformerFactory()
        response = self.client.get('/admin/shastra_compedium/performer/',
                                   follow=True)
        self.assertContains(response, obj.name)
        for style in obj.dance_styles.all():
            self.assertContains(response, style.name)

    def test_get_exampleimage(self):
        self.img1 = set_image(folder_name="PositionImageUploads")
        combo = CombinationDetailFactory()
        obj = ExampleImageFactory(image=self.img1)
        obj.combinations.add(combo)
        response = self.client.get('/admin/shastra_compedium/exampleimage/',
                                   follow=True)
        self.assertContains(response, obj.position.name)
        self.assertContains(response, '<td class="field-combo_count">1</td>')

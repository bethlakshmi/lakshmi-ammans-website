from django.views.generic.edit import (
    CreateView,
    UpdateView,
)
from django_addanother.views import CreatePopupMixin, UpdatePopupMixin
from shastra_compedium.models import ExampleImage
from django.urls import reverse_lazy
from shastra_compedium.site_text import make_example_image_messages
from shastra_compedium.views import ShastraFormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from shastra_compedium.forms import ImageForm


class ExampleImageCreate(LoginRequiredMixin,
                         CreatePopupMixin,
                         ShastraFormMixin,
                         CreateView):
    model = ExampleImage
    template_name = 'shastra_compedium/modal_make_form.tmpl'
    success_url = reverse_lazy('position_list',
                               urlconf="shastra_compedium.urls")
    page_title = 'Example Image'
    view_title = 'Create Example Image'
    valid_message = make_example_image_messages['create_success']
    intro_message = make_example_image_messages['create_intro']
    fields = ['position', 'general', 'details', 'dance_style', 'performer']


class ExampleImageUpdate(LoginRequiredMixin,
                         UpdatePopupMixin,
                         ShastraFormMixin,
                         UpdateView):
    model = ExampleImage
    template_name = 'shastra_compedium/modal_make_form.tmpl'
    success_url = reverse_lazy('position_list',
                               urlconf="shastra_compedium.urls")
    page_title = 'Example Image'
    view_title = 'Update Example Image'
    valid_message = make_example_image_messages['edit_success']
    intro_message = make_example_image_messages['edit_intro']
    form_class = ImageForm

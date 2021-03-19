from django.views.generic.edit import (
    CreateView,
    UpdateView,
)
from django_addanother.views import CreatePopupMixin, UpdatePopupMixin
from shastra_compedium.models import Shastra
from django.urls import reverse_lazy
from shastra_compedium.site_text import make_shastra_messages
from shastra_compedium.views import ShastraFormMixin


class ShastraCreate(CreatePopupMixin,
                    ShastraFormMixin,
                    CreateView):
    model = Shastra
    template_name = 'shastra_compedium/modal_make_form.tmpl'
    success_url = reverse_lazy('shastra-add', urlconf="shastra_compedium.urls")
    page_title = 'Shastra'
    view_title = 'Create Shastra'
    valid_message = make_shastra_messages['create_success']
    intro_message = make_shastra_messages['create_intro']
    required_css_class = 'required'
    error_css_class = 'error'
    fields = ['title',
              'author',
              'language',
              'min_age',
              'max_age',
              'description']

    def get_success_url(self):
        return self.request.GET.get('next', self.success_url)


class ShastraUpdate(UpdatePopupMixin,
                    ShastraFormMixin,
                    UpdateView):
    model = Shastra
    template_name = 'shastra_compedium/modal_make_form.tmpl'
    success_url = reverse_lazy('shastra-add', urlconf="shastra_compedium.urls")
    page_title = 'Shastra'
    view_title = 'Update Shastra'
    valid_message = make_shastra_messages['edit_success']
    intro_message = make_shastra_messages['edit_intro']
    required_css_class = 'required'
    error_css_class = 'error'
    fields = ['title',
              'author',
              'language',
              'min_age',
              'max_age',
              'description']

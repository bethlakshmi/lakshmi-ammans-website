from django.views.generic.edit import (
    CreateView,
    UpdateView,
)
from django_addanother.views import CreatePopupMixin, UpdatePopupMixin
from shastra_compedium.models import Source
from django.urls import reverse_lazy
from shastra_compedium.site_text import make_source_messages
from shastra_compedium.views import ShastraFormMixin
from shastra_compedium.forms import SourceForm


class SourceCreate(CreatePopupMixin,
                   ShastraFormMixin,
                   CreateView):
    model = Source
    template_name = 'shastra_compedium/modal_make_form.tmpl'
    success_url = reverse_lazy('source-add', urlconf="shastra_compedium.urls")
    page_title = 'Source'
    view_title = 'Create Source'
    valid_message = make_source_messages['create_success']
    intro_message = make_source_messages['create_intro']
    form_class = SourceForm

    def get_success_url(self):
        return self.request.GET.get('next', self.success_url)


class SourceUpdate(UpdatePopupMixin,
                   ShastraFormMixin,
                   UpdateView):
    model = Source
    template_name = 'shastra_compedium/modal_make_form.tmpl'
    success_url = reverse_lazy('source-add', urlconf="shastra_compedium.urls")
    page_title = 'Source'
    view_title = 'Update Source'
    valid_message = make_source_messages['edit_success']
    intro_message = make_source_messages['edit_intro']
    form_class = SourceForm

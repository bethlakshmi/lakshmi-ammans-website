from django.views.generic.edit import (
    CreateView,
    UpdateView,
)
from django_addanother.views import CreatePopupMixin, UpdatePopupMixin
from shastra_compedium.models import Subject
from django.urls import reverse_lazy
from shastra_compedium.site_text import make_subject_messages
from shastra_compedium.views import ShastraFormMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class SubjectCreate(LoginRequiredMixin,
                    CreatePopupMixin,
                    ShastraFormMixin,
                    CreateView):
    model = Subject
    template_name = 'shastra_compedium/modal_make_form.tmpl'
    success_url = reverse_lazy('combo_list',
                               urlconf="shastra_compedium.urls")
    page_title = 'Subject'
    view_title = 'Create Subject'
    valid_message = make_subject_messages['create_success']
    intro_message = make_subject_messages['create_intro']
    fields = ['name', 'category']


class SubjectUpdate(LoginRequiredMixin,
                    UpdatePopupMixin,
                    ShastraFormMixin,
                    UpdateView):
    model = Subject
    template_name = 'shastra_compedium/modal_make_form.tmpl'
    success_url = reverse_lazy('combo_list',
                               urlconf="shastra_compedium.urls")
    page_title = 'Subject'
    view_title = 'Update Subject'
    valid_message = make_subject_messages['edit_success']
    intro_message = make_subject_messages['edit_intro']
    fields = ['name', 'category']

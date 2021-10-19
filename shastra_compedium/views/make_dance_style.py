from django.views.generic.edit import (
    CreateView,
    UpdateView,
)
from django_addanother.views import CreatePopupMixin, UpdatePopupMixin
from shastra_compedium.models import DanceStyle
from django.urls import reverse_lazy
from shastra_compedium.site_text import make_dance_style_messages
from shastra_compedium.views import ShastraFormMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class DanceStyleCreate(LoginRequiredMixin,
                      CreatePopupMixin,
                      ShastraFormMixin,
                      CreateView):
    model = DanceStyle
    template_name = 'shastra_compedium/modal_make_form.tmpl'
    success_url = reverse_lazy('position_list',
                               urlconf="shastra_compedium.urls")
    page_title = 'DanceStyle'
    view_title = 'Create Dance Style'
    valid_message = make_dance_style_messages['create_success']
    intro_message = make_dance_style_messages['create_intro']
    fields = ['name', 'description']


class DanceStyleUpdate(LoginRequiredMixin,
                      UpdatePopupMixin,
                      ShastraFormMixin,
                      UpdateView):
    model = DanceStyle
    template_name = 'shastra_compedium/modal_make_form.tmpl'
    success_url = reverse_lazy('position_list',
                               urlconf="shastra_compedium.urls")
    page_title = 'DanceStyle'
    view_title = 'Update Dance Style'
    valid_message = make_dance_style_messages['edit_success']
    intro_message = make_dance_style_messages['edit_intro']
    fields = ['name', 'description']

from django.views.generic.edit import (
    CreateView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from reference_manager.texts import make_source_messages
from reference_manager.forms import URLSourceForm
from reference_manager.models import URLSource


class URLSourceCreate(LoginRequiredMixin,
                      CreateView):
    model = URLSource
    template_name = 'reference_manager/simple_form.tmpl'
    success_url = "/"
    valid_message = make_source_messages['create_success']
    intro_message = make_source_messages['create_intro']
    form_class = URLSourceForm


class URLSourceUpdate(LoginRequiredMixin,
                      UpdateView):
    model = URLSource
    template_name = 'reference_manager/simple_form.tmpl'
    success_url = "/"
    valid_message = make_source_messages['edit_success']
    intro_message = make_source_messages['edit_intro']
    form_class = URLSourceForm

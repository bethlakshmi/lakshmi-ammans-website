from django.views.generic.edit import (
    CreateView,
    UpdateView,
)
from django_addanother.views import CreatePopupMixin, UpdatePopupMixin
from shastra_compedium.models import Performer
from django.urls import reverse_lazy
from shastra_compedium.site_text import make_performer_messages
from shastra_compedium.views import ShastraFormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from shastra_compedium.forms import PerformerForm


class PerformerCreate(LoginRequiredMixin,
                      CreatePopupMixin,
                      ShastraFormMixin,
                      CreateView):
    model = Performer
    template_name = 'shastra_compedium/modal_make_form.tmpl'
    success_url = reverse_lazy('position_list',
                               urlconf="shastra_compedium.urls")
    page_title = 'Performer'
    view_title = 'Create Performer'
    valid_message = make_performer_messages['create_success']
    intro_message = make_performer_messages['create_intro']
    form_class = PerformerForm

    def get_initial(self):
        initial = super().get_initial()
        initial['contact'] = self.request.user
        return initial

class PerformerUpdate(LoginRequiredMixin,
                      UpdatePopupMixin,
                      ShastraFormMixin,
                      UpdateView):
    model = Performer
    template_name = 'shastra_compedium/modal_make_form.tmpl'
    success_url = reverse_lazy('position_list',
                               urlconf="shastra_compedium.urls")
    page_title = 'Performer'
    view_title = 'Update Performer'
    valid_message = make_performer_messages['edit_success']
    intro_message = make_performer_messages['edit_intro']
    form_class = PerformerForm

    def get_queryset(self):
        return self.model.objects.filter(contact=self.request.user)

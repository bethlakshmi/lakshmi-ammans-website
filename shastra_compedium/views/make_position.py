from django.views.generic.edit import (
    CreateView,
    UpdateView,
)
from django_addanother.views import CreatePopupMixin, UpdatePopupMixin
from shastra_compedium.models import Position
from django.urls import reverse_lazy
from shastra_compedium.site_text import make_position_messages
from shastra_compedium.views import ShastraFormMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class PositionCreate(LoginRequiredMixin,
                     CreatePopupMixin,
                     ShastraFormMixin,
                     CreateView):
    model = Position
    template_name = 'shastra_compedium/modal_make_form.tmpl'
    success_url = reverse_lazy('position_list',
                               urlconf="shastra_compedium.urls")
    page_title = 'Position'
    view_title = 'Create Position'
    valid_message = make_position_messages['create_success']
    intro_message = make_position_messages['create_intro']
    fields = ['name', 'category', 'order']

    def get_success_url(self):
        return self.request.GET.get('next', self.success_url)

    def get_initial(self):
        initial = super().get_initial()
        if 'order' in self.kwargs:
            initial['order'] = int(self.kwargs['order'])
        if 'category' in self.kwargs:
            initial['category'] = int(self.kwargs['category'])
        return initial


class PositionUpdate(LoginRequiredMixin,
                     UpdatePopupMixin,
                     ShastraFormMixin,
                     UpdateView):
    model = Position
    template_name = 'shastra_compedium/modal_make_form.tmpl'
    success_url = reverse_lazy('position_list',
                               urlconf="shastra_compedium.urls")
    page_title = 'Position'
    view_title = 'Update Position'
    valid_message = make_position_messages['edit_success']
    intro_message = make_position_messages['edit_intro']
    fields = ['name', 'category', 'order']

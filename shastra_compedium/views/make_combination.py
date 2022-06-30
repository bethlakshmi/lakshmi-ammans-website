from django.views.generic.edit import UpdateView
from django_addanother.views import CreatePopupMixin, UpdatePopupMixin
from shastra_compedium.models import CombinationDetail
from django.urls import reverse_lazy
from shastra_compedium.site_text import make_combination_messages
from shastra_compedium.views import ShastraFormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from shastra_compedium.forms import CombinationDetailEditForm


class CombinationUpdate(LoginRequiredMixin,
                        UpdatePopupMixin,
                        ShastraFormMixin,
                        UpdateView):
    model = CombinationDetail
    template_name = 'shastra_compedium/modal_make_form.tmpl'
    success_url = reverse_lazy('combo_list',
                               urlconf="shastra_compedium.urls")
    page_title = 'Combination'
    view_title = 'Update Combination'
    valid_message = make_combination_messages['edit_success']
    intro_message = make_combination_messages['edit_intro']
    form_class = CombinationDetailEditForm

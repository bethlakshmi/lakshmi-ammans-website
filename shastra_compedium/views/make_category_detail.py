from django.views.generic.edit import UpdateView
from shastra_compedium.models import CategoryDetail
from django.urls import reverse_lazy
from shastra_compedium.site_text import make_category_detail_messages
from shastra_compedium.views import ShastraFormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from shastra_compedium.forms import ChapterFormBasics


class CategoryDetailUpdate(LoginRequiredMixin,
                     ShastraFormMixin,
                     UpdateView):
    model = CategoryDetail
    template_name = 'shastra_compedium/modal_make_form.tmpl'
    success_url = reverse_lazy('source_list',
                               urlconf="shastra_compedium.urls")
    page_title = 'Edit Chapter'
    view_title = 'Update Chapter'
    valid_message = make_category_detail_messages['edit_success']
    intro_message = make_category_detail_messages['edit_intro']
    form_class = ChapterFormBasics

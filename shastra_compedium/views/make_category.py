from django.views.generic.edit import (
    CreateView,
    UpdateView,
)
from django_addanother.views import CreatePopupMixin, UpdatePopupMixin
from shastra_compedium.models import Category
from django.urls import reverse_lazy
from shastra_compedium.site_text import make_category_messages
from shastra_compedium.views import ShastraFormMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class CategoryCreate(LoginRequiredMixin,
                     CreatePopupMixin,
                     ShastraFormMixin,
                     CreateView):
    model = Category
    template_name = 'shastra_compedium/modal_make_form.tmpl'
    success_url = reverse_lazy('position_list',
                               urlconf="shastra_compedium.urls")
    page_title = 'Category'
    view_title = 'Create Category'
    valid_message = make_category_messages['create_success']
    intro_message = make_category_messages['create_intro']
    fields = ['name', 'description']

    def get_success_url(self):
        return self.request.GET.get('next', self.success_url)


class CategoryUpdate(LoginRequiredMixin,
                     UpdatePopupMixin,
                     ShastraFormMixin,
                     UpdateView):
    model = Category
    template_name = 'shastra_compedium/modal_make_form.tmpl'
    success_url = reverse_lazy('position_list',
                               urlconf="shastra_compedium.urls")
    page_title = 'Category'
    view_title = 'Update Category'
    valid_message = make_category_messages['edit_success']
    intro_message = make_category_messages['edit_intro']
    fields = ['name', 'description']

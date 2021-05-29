from django.views.generic.edit import (
    CreateView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from reference_manager.models import Tag


class TagCreate(LoginRequiredMixin,
                      CreateView):
    model = Tag
    template_name = 'reference_manager/simple_form.tmpl'
    success_url = "/"
    fields = ['name', 'description', 'slug']


class TagUpdate(LoginRequiredMixin,
                      UpdateView):
    model = Tag
    template_name = 'reference_manager/simple_form.tmpl'
    success_url = "/"
    fields = ['name', 'description', 'slug']

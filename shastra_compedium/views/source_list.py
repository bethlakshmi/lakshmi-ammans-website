from django.views.generic import View
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from shastra_compedium.models import (
    Shastra,
    Source,
)
from django.urls import reverse
from shastra_compedium.views import GenericList


class SourceList(GenericList):
    template = 'shastra_compedium/source_list.tmpl'
    title = "List of Sources"

    def get_context_dict(self):
        context = super(SourceList, self).get_context_dict()
        context['shastras'] = Shastra.objects.filter(sources=None)
        return context

    def get_list(self):
        return Source.objects.all()

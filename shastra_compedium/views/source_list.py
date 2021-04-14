from django.views.generic.list import ListView
from shastra_compedium.models import Source


class SourceList(ListView):

    model = Source
    template = "shastra_compedium/source_list.tmpl"

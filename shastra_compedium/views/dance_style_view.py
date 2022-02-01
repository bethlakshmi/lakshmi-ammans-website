from django.views.generic.detail import DetailView
from shastra_compedium.models import DanceStyle

class DanceStyleView(DetailView):

    model = DanceStyle
    template_name = 'shastra_compedium/dancestyle_view.tmpl'

from django.views.generic.detail import DetailView
from shastra_compedium.models import Performer

class PerformerView(DetailView):

    model = Performer
    template_name = 'shastra_compedium/performer_view.tmpl'

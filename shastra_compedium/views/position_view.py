from django.views.generic.detail import DetailView
from shastra_compedium.models import Position

class PositionView(DetailView):

    model = Position
    template_name = 'shastra_compedium/position_view.tmpl'

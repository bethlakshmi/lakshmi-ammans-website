from dal import autocomplete
from shastra_compedium.models import Position


class PositionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Position.objects.none()

        qs = Position.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

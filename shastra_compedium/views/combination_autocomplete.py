from dal import autocomplete
from shastra_compedium.models import CombinationDetail


class CombinationAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return CombinationDetail.objects.none()

        qs = CombinationDetail.objects.all()

        if self.q:
            qs = qs.filter(contents__icontains=self.q)
        return qs

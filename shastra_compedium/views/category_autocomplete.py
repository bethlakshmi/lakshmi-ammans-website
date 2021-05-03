from dal import autocomplete
from shastra_compedium.models import Category


class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Position.objects.none()

        qs = Category.objects.all().order_by('name')

        if self.q:
            qs = qs.filter(name__icontains=self.q).order_by('name')

        return qs

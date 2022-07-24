from dal import autocomplete
from shastra_compedium.models import Subject


class SubjectAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Subject.objects.none()

        qs = Subject.objects.all().order_by('name')

        if self.q:
            qs = qs.filter(name__icontains=self.q).order_by('name')

        return qs

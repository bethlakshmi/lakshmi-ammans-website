from dal import autocomplete
from shastra_compedium.models import PositionDetail


class PositionDetailAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return PositionDetail.objects.none()

        qs = PositionDetail.objects.all()
        sources = self.forwarded.get('sources')
        if sources:
            qs = qs.filter(sources__pk__in=sources)

        position = self.forwarded.get('position')
        if position:
            qs = qs.exclude(position__pk=position)

        position_limit = self.forwarded.get('position_only')
        if position_limit:
            qs = qs.filter(position__pk=position_limit)

        detail_id = self.forwarded.get('id')
        if detail_id:
            qs = qs.exclude(id=detail_id)

        usage = self.forwarded.get('usage')
        if usage:
            qs = qs.filter(usage=usage)

        if self.q:
            qs = qs.filter(position__name__icontains=self.q)

        return qs

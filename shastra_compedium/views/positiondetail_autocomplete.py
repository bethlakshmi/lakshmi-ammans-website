from dal import autocomplete
from shastra_compedium.models import PositionDetail
from django.utils.html import strip_tags
from django.utils.html import format_html
from django.db.models import Q


class PositionDetailAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return PositionDetail.objects.none()

        qs = PositionDetail.objects.all()
        sources = self.forwarded.get('sources')
        if sources:
            if isinstance(sources, list):
                qs = qs.filter(sources__pk__in=sources)
            # ugly but needed until refactor to remove many to many here
            else:
                qs = qs.filter(sources__pk__in=[sources])

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
            qs = qs.filter(Q(position__name__icontains=self.q) |
                           Q(position__contents__icontains=self.q))

        return qs

class PositionDetailExampleAutocomplete(PositionDetailAutocomplete):
    # same search logic, but uses formatting for choices that work well with 
    # example image configurations
    def get_result_label(self, result):
        return format_html('%s - %s - %s' % (
            result.sources.first().shastra.initials,
            result.verses(),
            strip_tags(result.contents[3:28])))

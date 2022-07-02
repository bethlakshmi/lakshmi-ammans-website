from dal import autocomplete
from shastra_compedium.models import CombinationDetail
from django.utils.html import strip_tags
from django.utils.html import format_html


class CombinationAutocomplete(autocomplete.Select2QuerySetView):
    def get_result_label(self, result):
        return format_html('%s - %s - %s' % (
            result.sources.first().shastra.initials,
            result.verses(),
            strip_tags(result.contents[3:28])))

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return CombinationDetail.objects.none()

        qs = CombinationDetail.objects.all()

        if self.q:
            qs = qs.filter(contents__icontains=self.q)
        return qs

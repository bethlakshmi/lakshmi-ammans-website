from shastra_compedium.models import (
    CategoryDetail,
    CombinationDetail,
    PositionDetail,
    Shastra,
    Source,
)
from shastra_compedium.views import GenericList
from django.db.models import Count


class SourceList(GenericList):
    template = 'shastra_compedium/source_list.tmpl'
    title = "List of Sources"

    def get_context_dict(self):
        context = super(SourceList, self).get_context_dict()
        context['shastra_ids'] = []
        context['shastras'] = Shastra.objects.filter(sources=None)
        if self.changed_obj == "Shastra":
            context['shastra_ids'] = context['changed_ids']
            context['changed_ids'] = []
        if self.changed_obj == "CategoryDetail":
            context['categorydetail_ids'] = context['changed_ids']
            context['changed_ids'] = list(CategoryDetail.objects.filter(
                pk__in=context['categorydetail_ids']).values_list(
                'sources__pk',
                flat=True))
        if self.changed_obj == "Category":
            context['changed_ids'] = []
        return context

    def get_list(self):
        source_dict = {}
        for cat_detail in CategoryDetail.objects.all().order_by(
                'category__name'):
            for source in cat_detail.sources.all():
                # assumption - if there are two details for a category, they
                # both have the same chapter number.  If that's wrong, we'll
                # be missing some # of combinations
                combo_count = CombinationDetail.objects.filter(
                    chapter=cat_detail.chapter,
                    sources__in=[source]).count()
                if source in source_dict:
                    if cat_detail.category in source_dict[source]:
                        source_dict[source][cat_detail.category][
                            'details'] += [cat_detail]
                    else:
                        source_dict[source][cat_detail.category] = {
                            'positions': [],
                            'details': [cat_detail],
                            'combos': combo_count}
                else:
                    source_dict[source] = {
                        cat_detail.category: {'positions': [],
                                              'details': [cat_detail],
                                              'combos': combo_count},
                    }
        for pos in PositionDetail.objects.all():
            for source in pos.sources.all():
                if source not in source_dict:
                    source_dict[source] = {}

                if pos.position.category in source_dict[source]:
                    if pos.position not in source_dict[source][
                            pos.position.category]['positions']:
                        source_dict[source][pos.position.category][
                            'positions'] += [pos.position]
                else:
                    combo_count = CombinationDetail.objects.filter(
                        chapter=pos.chapter,
                        sources__in=[source]).count()
                    source_dict[source][pos.position.category] = {
                        'positions': [pos.position],
                        'details': [],
                        'combos': combo_count}
        for source in Source.objects.filter(categorydetail=None,
                                            positiondetail=None):
            source_dict[source] = {'chapters': []}

        return source_dict

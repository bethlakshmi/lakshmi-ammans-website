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
                if source in source_dict:
                    if cat_detail.category in source_dict[source]:
                        source_dict[source][cat_detail.category][
                            'details'] += [cat_detail]
                    else:
                        source_dict[source][cat_detail.category] = {
                            'positions': [],
                            'details': [cat_detail],
                            'combos': 0}
                else:
                    source_dict[source] = {
                        cat_detail.category: {'positions': [],
                                              'details': [cat_detail],
                                              'combos': 0},
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
                    source_dict[source][pos.position.category] = {
                        'positions': [pos.position],
                        'details': [],
                        'combos': 0}
        for combo in CombinationDetail.objects.all():
            for source in combo.sources.all():
                if source not in source_dict:
                    source_dict[source] = {}

                category = "NONE"
                if combo.subject is not None:
                    category = combo.subject.category
                if category not in source_dict[source]:
                    source_dict[source][category] = {
                        'positions': [],
                        'details': [],
                        'combos': 0}
                source_dict[source][category]['combos'] = (
                    source_dict[source][category]['combos'] + 1)

        for source in Source.objects.filter(categorydetail=None,
                                            positiondetail=None):
            source_dict[source] = {'chapters': []}

        return source_dict

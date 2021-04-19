from django.views.generic import View
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from shastra_compedium.models import (
    CategoryDetail,
    PositionDetail,
    Shastra,
    Source,
)
from django.urls import reverse
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
                            'count': 0,
                            'details': [cat_detail]}
                else:
                    source_dict[source] = {
                            cat_detail.category: {'count': 0,
                                                  'details': [cat_detail]},
                    }
        for source in Source.objects.filter(categorydetail=None):
            source_dict[source] = {'chapters': []}
        for pos in PositionDetail.objects.all():
            for source in pos.sources.all():
                source_dict[source][pos.position.category][
                    'count'] = source_dict[source][pos.position.category][
                    'count'] + 1

        return source_dict

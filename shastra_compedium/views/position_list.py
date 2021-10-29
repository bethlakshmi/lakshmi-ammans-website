from django.views.generic import View
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from shastra_compedium.models import (
    PositionDetail,
    Shastra,
    Source,
)
from django.urls import reverse
from shastra_compedium.views import GenericList


class PositionList(GenericList):
    template = 'shastra_compedium/position_list.tmpl'
    title = "List of Positions"

    def get_context_dict(self):
        context = super(PositionList, self).get_context_dict()
        context['sources'] = Source.objects.all()
        context['shastras'] = Shastra.objects.all()
        if self.changed_obj == "Category":
            context['category_ids'] = context['changed_ids']
            context['changed_ids'] = []
        return context

    def get_list(self):
        details = {}
        for detail in PositionDetail.objects.filter(description__isnull=True):
            if detail.position not in details:
                details[detail.position] = {}
            for source in detail.sources.all():
                usage = detail.usage.replace(" ", "")
                if source not in details[detail.position]:
                    details[detail.position][source] = {usage: [detail],
                                                        'num_details': 0}
                elif usage not in details[detail.position][source]:
                    details[detail.position][source][usage] = [detail]
                else:
                    details[detail.position][source][usage] += [detail]
                details[detail.position][source]['num_details'] = details[
                    detail.position][source]['num_details'] + 1
        return details

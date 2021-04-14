from django.views.generic import View
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from shastra_compedium.models import (
    Position,
    PositionDetail,
    Source,
)
from django.urls import reverse


class PositionList(View):
    object_type = Position
    template = 'shastra_compedium/position_list.tmpl'
    title = "List of Positions"
    order_fields = ('category', 'order')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PositionList, self).dispatch(*args, **kwargs)

    def get_context_dict(self):
        return {
            'title': self.title,
            'page_title': self.title,
            'items': self.get_list(),
            'changed_id': self.changed_id,
            'error_id': self.error_id,
            'sources': Source.objects.all(),
            'path_list': [
                ("Postiion List",
                 reverse('position_list', urlconf='shastra_compedium.urls')),
                ("Source List",
                 reverse('source_list', urlconf='shastra_compedium.urls'))]
            }

    def get_list(self):
        details = {}
        for detail in PositionDetail.objects.all():
            if detail.position not in details:
                details[detail.position] = {}
            for source in detail.sources.all():
                if source not in details[detail.position]:
                    details[detail.position][source] = {detail.usage: detail}
                else:
                    details[detail.position][source][detail.usage] = detail
        return details

    @never_cache
    def get(self, request, *args, **kwargs):
        self.changed_id = int(request.GET.get('changed_id', default=-1))
        self.error_id = int(request.GET.get('error_id', default=-1))
        return render(request, self.template, self.get_context_dict())

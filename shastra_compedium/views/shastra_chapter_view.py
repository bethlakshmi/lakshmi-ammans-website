from django.views.generic import View
from django.shortcuts import render
from shastra_compedium.models import (
    Category,
    PositionDetail,
    Shastra,
    UserMessage,
)
from django.urls import reverse
from shastra_compedium.site_text import user_messages
from collections import OrderedDict


class ShastraChapterView(View):
    template = 'shastra_compedium/shastra_chapter.tmpl'
    source_align = {
        1: 12,
        2: 6,
        3: 4,
        4: 3,
        5: 2,
        6: 2,
    }

    def get_context_dict(self):
        shastra = Shastra.objects.get(pk=self.shastra_pk)
        category = Category.objects.get(pk=self.category_pk)
        details = OrderedDict()
        empty_source_dict = OrderedDict()

        for detail in PositionDetail.objects.filter(
                sources__shastra=shastra,
                position__category=category).order_by(
                "position__order",
                "sources__translator",
                "chapter",
                "verse_start",
                "pk"):
            # init the dict
            if detail.position not in details:
                details[detail.position] = {}
                for source in shastra.sources.all():
                    details[detail.position][source] = []
            # put the detail in the right place
            for source in detail.sources.filter(shastra=shastra):
                details[detail.position][source] += [detail]
        context = {
            'shastra': shastra,
            'category': category,
            'details': details,
            'source_size': self.source_align[shastra.sources.count()]
            }
        if self.__class__.__name__ in user_messages:
            context['instructions'] = UserMessage.objects.get_or_create(
                view=self.__class__.__name__,
                code="%s_INSTRUCTIONS" % self.__class__.__name__.upper(),
                defaults={
                    'summary': user_messages[self.__class__.__name__][
                        'summary'],
                    'description': user_messages[self.__class__.__name__][
                        'description']}
                )[0].description
        return context

    def get(self, request, *args, **kwargs):
        self.shastra_pk = kwargs.get("shastra_pk")
        self.category_pk = kwargs.get("category_pk")
        return render(request, self.template, self.get_context_dict())
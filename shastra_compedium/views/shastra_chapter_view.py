from django.views.generic import View
from django.shortcuts import render
from shastra_compedium.models import (
    Category,
    CategoryDetail,
    CombinationDetail,
    PositionDetail,
    Shastra,
    UserMessage,
)
from django.urls import reverse
from collections import OrderedDict
from django.shortcuts import get_object_or_404


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
    pic_size = {
        1: "col-6 col-md-4 col-lg-3 col-xl-2",
        2: "col-12 col-md-6 col-lg-4 col-xl-3",
        3: "col-12 col-lg-6 col-xl-4",
        4: "col-12 col-xl-6",
        5: "col-12",
        6: "col-12",
    }

    def get_context_dict(self):
        shastra = get_object_or_404(Shastra, pk=self.shastra_pk)
        category = get_object_or_404(Category, pk=self.category_pk)
        details = OrderedDict()
        empty_source_dict = OrderedDict()
        categorydetails = CategoryDetail.objects.filter(
            sources__shastra=shastra,
            category=category)
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
        combination_dict = OrderedDict()
        for combo in CombinationDetail.objects.filter(
                sources__shastra=shastra,
                chapter__in=categorydetails.values_list('chapter', flat=True)
                ).order_by("sources__translator", "chapter", "verse_start"):
            if combo.sources.first() not in combination_dict:
                combination_dict[combo.sources.first()] = [combo]
            else:
                combination_dict[combo.sources.first()] += [combo]

        context = {
            'shastra': shastra,
            'category': category,
            'categorydetails': categorydetails,
            'details': details,
            'combinations': combination_dict,
            'source_size': self.source_align[shastra.sources.count()],
            'pic_size': self.pic_size[shastra.sources.count()],
            }
        return context

    def get(self, request, *args, **kwargs):
        self.shastra_pk = kwargs.get("shastra_pk")
        self.category_pk = kwargs.get("category_pk")
        return render(request, self.template, self.get_context_dict())

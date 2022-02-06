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


class ShastraChapterView(View):
    def get_context_dict(self):
        context = {
            'shastra': Shastra.objects.get(self.shastra_pk),
            'category': Category.objects.get(self.category_pk),
            'details': self.get_list(),
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
        self.shastra_pk = request.GET.get('shastra_pk', default="")
        self.category_pk = request.GET.get('category_pk', default="")
        self.error_id = int(request.GET.get('error_id', default=-1))
        return render(request, self.template, self.get_context_dict())

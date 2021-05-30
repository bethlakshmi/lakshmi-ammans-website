from django.views.generic import View
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from shastra_compedium.models import (
    Shastra,
    Source,
    UserMessage,
)
from django.urls import reverse
from shastra_compedium.site_text import user_messages


class GenericList(View):
    #
    # this is an abstract class, to instantiate it, implement:
    # - implement get_list - the list to get, returns a list or queryset
    # - set template - best if it extends generic_list.tmpl
    # - set title
    # if you override get_context_dict, call this version first so that
    # path list is set centrally
    #

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GenericList, self).dispatch(*args, **kwargs)

    def get_context_dict(self):
        context = {
            'title': self.title,
            'page_title': self.title,
            'items': self.get_list(),
            'changed_ids': self.changed_ids,
            'error_id': self.error_id,
            'path_list': [
                ("Position List",
                 reverse('position_list', urlconf='shastra_compedium.urls')),
                ("Source List",
                 reverse('source_list', urlconf='shastra_compedium.urls'))]
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

    @never_cache
    def get(self, request, *args, **kwargs):
        self.changed_ids = eval(request.GET.get('changed_ids', default="[]"))
        self.changed_obj = request.GET.get('obj_type', default="")
        self.error_id = int(request.GET.get('error_id', default=-1))
        return render(request, self.template, self.get_context_dict())

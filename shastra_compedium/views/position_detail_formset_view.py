from extra_views import FormSetSuccessMessageMixin, ModelFormSetView
from django.urls import reverse_lazy
from shastra_compedium.models import (
    PositionDetail,
    UserMessage,
)
from shastra_compedium.site_text import edit_post_detail_messages
from shastra_compedium.forms import PositionDetailEditForm
from django.contrib.auth.mixins import LoginRequiredMixin


class PositionDetailFormSetView(LoginRequiredMixin,
                                FormSetSuccessMessageMixin,
                                ModelFormSetView):
    model = PositionDetail
    form_class = PositionDetailEditForm
    factory_kwargs = {'extra': 0}
    template_name = 'shastra_compedium/position_formset.tmpl'
    intro_message = edit_post_detail_messages['intro']
    page_title = "Position Details"
    view_title = "Edit Position Details"
    success_url = reverse_lazy('source_list', urlconf="shastra_compedium.urls")
    source_id = -1

    def get_context_data(self, **kwargs):
        msg = UserMessage.objects.get_or_create(
            view=self.__class__.__name__,
            code="INTRO",
            defaults={
                'summary': "Successful Submission",
                'description': self.intro_message})
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['title'] = self.view_title
        context['instructions'] = msg[0].description
        context['special_handling'] = True
        context['tiny_mce_width'] = 400
        context['return_url'] = self.request.GET.get('next', self.success_url)
        return context

    def get_queryset(self):
        query = super(PositionDetailFormSetView, self).get_queryset()
        if 'position_id' in self.kwargs:
            query = query.filter(position__id=self.kwargs['position_id'])
            self.changed_id = self.kwargs['position_id']
        if 'source_id' in self.kwargs:
            query = query.filter(sources__id=self.kwargs['source_id'])
            self.source_id = self.kwargs['source_id']
        if 'category_id' in self.kwargs:
            cat_id = self.kwargs['category_id']
            if len(cat_id) > 0:
                query = query.filter(position__category__id=cat_id)
            else:
                query = query.filter(position__category__isnull=True)
        return query

    def get_success_message(self, formset):
        names = []
        name_list = ""
        for form in formset.forms:
            if form.instance.position.name not in names:
                names += [form.instance.position.name]
        for name in names:
            if len(name_list) == 0:
                name_list = name
            else:
                name_list = "%s, %s" % (name, name_list)
        return '{} position details were updated.'.format(name_list)

    def get_success_url(self):
        return "%s?changed_ids=[%s]&obj_type=Position&source_id=%s" % (
            self.request.GET.get('next', self.success_url),
            self.changed_id,
            self.source_id)

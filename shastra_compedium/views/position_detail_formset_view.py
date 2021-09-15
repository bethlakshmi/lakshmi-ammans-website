from extra_views import FormSetSuccessMessageMixin, ModelFormSetView
from django.urls import reverse_lazy
from shastra_compedium.models import (
    PositionDetail,
    UserMessage,
)
from shastra_compedium.site_text import edit_post_detail_messages
from shastra_compedium.forms import PositionDetailEditForm


class PositionDetailFormSetView(FormSetSuccessMessageMixin, ModelFormSetView):
    model = PositionDetail
    form_class = PositionDetailEditForm
    factory_kwargs = {'extra': 0}
    template_name = 'shastra_compedium/position_formset.tmpl'
    intro_message = edit_post_detail_messages['intro']
    page_title = "Position Details"
    view_title = "Edit Position Details"
    success_url = reverse_lazy('source_list', urlconf="shastra_compedium.urls")

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
        return context

    def get_queryset(self):
        query = super(PositionDetailFormSetView, self).get_queryset()
        if 'position_id' in self.kwargs:
            query = query.filter(position__id=self.kwargs['position_id'])
        elif 'source_id' in self.kwargs and 'category_id' in self.kwargs:
            query = query.filter(sources__id=self.kwargs['source_id'])
            cat_id = self.kwargs['category_id']
            if len(cat_id) > 0:
                query = query.filter(
                   position__category__id=cat_id)                   
            else:
                query = query.filter(position__category__isnull=True)
        return query
            
    def get_success_message(self, formset):
        return '{} position details were updated.'.format(len(formset.forms))

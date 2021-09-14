from extra_views import ModelFormSetView
from django.urls import reverse_lazy
from shastra_compedium.models import (
    PositionDetail,
    UserMessage,
)
from shastra_compedium.site_text import edit_post_detail_messages
from shastra_compedium.forms import PositionDetailEditForm


class PositionDetailFormSetView(ModelFormSetView):
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
        context['view_title'] = self.view_title
        context['instructions'] = msg[0].description
        context['special_handling'] = True
        context['tiny_mce_width'] = 400
        return context

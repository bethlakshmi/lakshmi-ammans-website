from django.views.generic.edit import ModelFormMixin
from django.contrib import messages
from shastra_compedium.models import UserMessage


class ShastraFormMixin(ModelFormMixin):
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
        context['intro_text'] = msg[0].description
        context['form'].required_css_class = 'required'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        msg = UserMessage.objects.get_or_create(
            view=self.__class__.__name__,
            code="SUCCESS",
            defaults={
                'summary': "Successful Submission",
                'description': self.valid_message})
        messages.success(self.request, msg[0].description % str(self.object))
        return response

    def get_success_url(self):
        return "%s?changed%s_id=%d" % (
            self.request.GET.get('next', self.success_url),
            self.object.__class__.__name__.lower(),
            self.object.pk)

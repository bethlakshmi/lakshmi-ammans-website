from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from shastra_compedium.forms import ChapterForm
from shastra_compedium.models import CategoryDetail
from shastra_compedium.views import ShastraFormMixin
from shastra_compedium.site_text import make_chapter_messages


class UploadChapter(LoginRequiredMixin, ShastraFormMixin, CreateView):
    model = CategoryDetail
    template_name = 'shastra_compedium/generic_wizard.tmpl'
    form_class = ChapterForm
    success_url = '/'
    page_title = 'Upload Chapter'
    view_title = 'Upload Chapter'
    valid_message = make_chapter_messages['upload_success']
    intro_message = make_chapter_messages['upload_intro']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtitle'] = "Set up chapter details and upload text"
        context['first'] = True
        return context

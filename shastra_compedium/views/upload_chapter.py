from django.views.generic.edit import CreateView
from shastra_compedium.forms import ChapterForm
from shastra_compedium.models import CategoryDetail


class UploadChapter(CreateView):
    model = CategoryDetail
    template_name = 'shastra_compedium/generic_wizard.tmpl'
    form_class = ChapterForm
    success_url = '/set_verses/'

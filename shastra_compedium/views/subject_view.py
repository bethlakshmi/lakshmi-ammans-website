from django.views.generic.detail import DetailView
from shastra_compedium.models import Subject


class SubjectView(DetailView):

    model = Subject
    template_name = 'shastra_compedium/subject_view.tmpl'

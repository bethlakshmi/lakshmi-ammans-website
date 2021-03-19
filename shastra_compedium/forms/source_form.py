from django.forms import (
    ModelForm,
    Select,
)
from shastra_compedium.models import Source
from django_addanother.widgets import AddAnotherEditSelectedWidgetWrapper
from django.urls import reverse_lazy


class SourceForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'

    class Meta:
        model = Source
        fields = ['title',
                  'shastra',
                  'translation_language',
                  'translator',
                  'isbn',
                  'bibliography',
                  'url']
        labels = {'url': 'URL'}
        help_texts = {'url': 'Place to buy or read book.'}
        widgets = {
            'category': AddAnotherEditSelectedWidgetWrapper(
                Select,
                reverse_lazy('category-add', urlconf='shastra_compedium.urls'),
                reverse_lazy('category-update',
                             urlconf='shastra_compedium.urls',
                             args=['__fk__'])),
            }

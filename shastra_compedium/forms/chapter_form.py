from django.forms import (
    CharField,
    ModelForm,
    Select,
    SelectMultiple,
)
from shastra_compedium.models import CategoryDetail
from django_addanother.widgets import AddAnotherEditSelectedWidgetWrapper
from django.urls import reverse_lazy


class ChapterForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'
    position_text = CharField(required=True, label="Contents of Chapter")

    class Meta:
        model = CategoryDetail
        fields = ['sources',
                  'category',
                  'usage',
                  'chapter',
                  'verse_start',
                  'verse_end',
                  'contents',
                  ]
        help_texts = {
            'sources': 'To edit a source, pick a single item before ' +
            'clicking the pencil.'}
        widgets = {
            'category': AddAnotherEditSelectedWidgetWrapper(
                Select,
                reverse_lazy('category-add', urlconf='shastra_compedium.urls'),
                reverse_lazy('category-update',
                             urlconf='shastra_compedium.urls',
                             args=['__fk__'])),
            'sources': AddAnotherEditSelectedWidgetWrapper(
                SelectMultiple,
                reverse_lazy('source-add', urlconf='shastra_compedium.urls'),
                reverse_lazy('source-update',
                             urlconf='shastra_compedium.urls',
                             args=['__fk__'])),
            }

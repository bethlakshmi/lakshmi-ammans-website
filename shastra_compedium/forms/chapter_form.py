from django.forms import (
    CharField,
    ModelForm,
    Select,
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
        widgets = {
            'category': AddAnotherEditSelectedWidgetWrapper(
                Select,
                reverse_lazy('category-add', urlconf='shastra_compedium.urls'),
                reverse_lazy('category-update',
                             urlconf='shastra_compedium.urls',
                             args=['__fk__'])),
            }

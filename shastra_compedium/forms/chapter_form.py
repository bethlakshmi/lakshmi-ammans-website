from django.forms import (
    CharField,
    ModelForm,
)
from shastra_compedium.models import CategoryDetail


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

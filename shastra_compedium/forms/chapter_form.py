from django.forms import (
    CharField,
    HiddenInput,
    IntegerField,
    ModelForm,
    Select,
    SelectMultiple,
    Textarea,
)
from shastra_compedium.models import CategoryDetail
from django_addanother.widgets import AddAnotherEditSelectedWidgetWrapper
from django.urls import reverse_lazy


class ChapterFormBasics(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'
    contents = CharField(
        widget=Textarea(attrs={'class': 'admin-tiny-mce'}),
        required=True,
        label="Chapter Intro",
        help_text='Source text for this chapter.',
        initial=" ")
    chapter = IntegerField(required=True)

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
        labels = {'contents': 'Chapter Intro'}
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


class ChapterForm(ChapterFormBasics):
    step = IntegerField(widget=HiddenInput(), initial=0)
    position_text = CharField(widget=Textarea(attrs={'cols': 86}),
                              required=True,
                              label="Contents of Chapter")

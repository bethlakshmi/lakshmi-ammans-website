from django.forms import (
    CharField,
    ModelForm,
    NumberInput,
    Textarea,
)
from shastra_compedium.models import CombinationDetail
from dal import autocomplete
from django_addanother.widgets import AddAnotherEditSelectedWidgetWrapper
from django.urls import reverse_lazy


class CombinationDetailEditForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'
    contents = CharField(
        widget=Textarea(attrs={'class': 'admin-tiny-mce'}),
        required=True,
        initial=" ")

    class Meta:
        model = CombinationDetail
        fields = [
            'sources',
            'chapter',
            'verse_start',
            'verse_end',
            'usage',
            'subject',
            'positions',
            'contents',
            ]
        widgets = {
            'chapter': NumberInput(attrs={'style': 'width: 50px'}),
            'verse_start': NumberInput(attrs={'style': 'width: 50px'}),
            'verse_end': NumberInput(attrs={'style': 'width: 50px'}),
            'positions': autocomplete.ModelSelect2Multiple(
                    url='position-autocomplete'),
            'subject': AddAnotherEditSelectedWidgetWrapper(
                autocomplete.ModelSelect2(url='subject-autocomplete'),
                reverse_lazy('subject-add', urlconf='shastra_compedium.urls'),
                reverse_lazy('subject-update',
                             urlconf='shastra_compedium.urls',
                             args=['__fk__'])),
            }

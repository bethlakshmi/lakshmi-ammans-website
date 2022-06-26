from django.forms import (
    CharField,
    HiddenInput,
    ModelForm,
    MultipleHiddenInput,
    NumberInput,
    Textarea,
)
from shastra_compedium.models import CombinationDetail
from dal import autocomplete


class CombinationDetailForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'
    contents = CharField(
        widget=Textarea(attrs={'class': 'admin-tiny-mce'}),
        required=False,
        initial=" ")

    class Meta:
        model = CombinationDetail
        fields = [
            'positions',
            'sources',
            'chapter',
            'verse_start',
            'verse_end',
            'usage',
            'contents',
            ]
        widgets = {
            'chapter': NumberInput(attrs={'style': 'width: 50px'}),
            'verse_start': NumberInput(attrs={'style': 'width: 50px'}),
            'verse_end': NumberInput(attrs={'style': 'width: 50px'}),
            'usage': HiddenInput(),
            'sources': MultipleHiddenInput(),
            'positions': autocomplete.ModelSelect2Multiple(
                    url='position-autocomplete'),
            }

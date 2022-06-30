from django.forms import (
    CharField,
    ModelForm,
    NumberInput,
    Textarea,
)
from shastra_compedium.models import CombinationDetail
from dal import autocomplete


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
            'positions',
            'contents',
            ]
        widgets = {
            'chapter': NumberInput(attrs={'style': 'width: 50px'}),
            'verse_start': NumberInput(attrs={'style': 'width: 50px'}),
            'verse_end': NumberInput(attrs={'style': 'width: 50px'}),
            'positions': autocomplete.ModelSelect2Multiple(
                    url='position-autocomplete'),
            }

from django.forms import (
    CharField,
    HiddenInput,
    ModelForm,
    NumberInput,
    Textarea,
)
from shastra_compedium.models import PositionDetail


class PositionDetailForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'
    posture = CharField(
        widget=Textarea(attrs={'class': 'admin-tiny-mce'}),
        required=True,
        initial=" ")

    class Meta:
        model = PositionDetail
        fields = [
            'position',
            'chapter',
            'verse_start',
            'verse_end',
            'usage',
            'contents',
            ]
        widgets = {
            'contents': Textarea(attrs={'class': 'admin-tiny-mce'}),
            'chapter': NumberInput(attrs={'style': 'width: 50px'}),
            'verse_start': NumberInput(attrs={'style': 'width: 50px'}),
            'verse_end': NumberInput(attrs={'style': 'width: 50px'}),
            'usage': HiddenInput(),
            }
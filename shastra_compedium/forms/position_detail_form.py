from django.forms import (
    CharField,
    HiddenInput,
    ModelForm,
    MultipleHiddenInput,
    NumberInput,
    Textarea,
)
from shastra_compedium.models import PositionDetail
from dal import autocomplete
from django_addanother.widgets import AddAnotherEditSelectedWidgetWrapper
from django.urls import reverse_lazy


class PositionDetailForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'
    posture = CharField(
        widget=Textarea(attrs={'class': 'admin-tiny-mce'}),
        required=False,
        initial=" ")
    contents = CharField(
        widget=Textarea(attrs={'class': 'admin-tiny-mce'}),
        required=False,
        initial=" ")

    class Meta:
        model = PositionDetail
        fields = [
            'position',
            'sources',
            'chapter',
            'verse_start',
            'verse_end',
            'usage',
            'contents',
            ]
        widgets = {
            'position': AddAnotherEditSelectedWidgetWrapper(
                autocomplete.ModelSelect2(url='position-autocomplete'),
                reverse_lazy('position-add', urlconf='shastra_compedium.urls'),
                reverse_lazy('position-update',
                             urlconf='shastra_compedium.urls',
                             args=['__fk__'])),
            'chapter': NumberInput(attrs={'style': 'width: 50px'}),
            'verse_start': NumberInput(attrs={'style': 'width: 50px'}),
            'verse_end': NumberInput(attrs={'style': 'width: 50px'}),
            'usage': HiddenInput(),
            'sources': MultipleHiddenInput(),
            }
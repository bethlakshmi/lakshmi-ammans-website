from django.forms import (
    CharField,
    ModelMultipleChoiceField,
    ModelForm,
    MultipleHiddenInput,
    NumberInput,
    Textarea,
)
from shastra_compedium.models import (
    CombinationDetail,
    Position,
)
from dal import autocomplete
from django_addanother.widgets import AddAnotherEditSelectedWidgetWrapper
from django.urls import reverse_lazy


class CombinationDetailForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'
    contents = CharField(
        widget=Textarea(attrs={'class': 'admin-tiny-mce'}),
        required=False,
        initial=" ")
    positions = ModelMultipleChoiceField(
        widget=autocomplete.ModelSelect2Multiple(url='position-autocomplete'),
        required=False,
        queryset=Position.objects.all())

    class Meta:
        model = CombinationDetail
        fields = [
            'positions',
            'sources',
            'chapter',
            'verse_start',
            'verse_end',
            'usage',
            'subject',
            'contents',
            ]
        widgets = {
            'chapter': NumberInput(attrs={'style': 'width: 50px'}),
            'verse_start': NumberInput(attrs={'style': 'width: 50px'}),
            'verse_end': NumberInput(attrs={'style': 'width: 50px'}),
            'sources': MultipleHiddenInput(),
            'subject': AddAnotherEditSelectedWidgetWrapper(
                autocomplete.ModelSelect2(url='subject-autocomplete'),
                reverse_lazy('subject-add', urlconf='shastra_compedium.urls'),
                reverse_lazy('subject-update',
                             urlconf='shastra_compedium.urls',
                             args=['__fk__'])),
            }

from django.forms import (
    CharField,
    ChoiceField,
    HiddenInput,
    ModelChoiceField,
    ModelForm,
    NumberInput,
    SelectMultiple,
    Textarea,
)
from shastra_compedium.models import (
    Position,
    PositionDetail,
)
from dal import (
    autocomplete,
    forward
)
from django_addanother.widgets import AddAnotherEditSelectedWidgetWrapper
from django.urls import reverse_lazy


class DescriptionChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s - %s - %s..." % (
            obj.verses(),
            obj.position.name,
            obj.contents[3:28])


class PositionDetailEditForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'
    contents = CharField(
        widget=Textarea(attrs={'class': 'admin-tiny-mce'}),
        required=False,
        initial=" ")
    position = ModelChoiceField(
        widget=AddAnotherEditSelectedWidgetWrapper(
            autocomplete.ModelSelect2(url='position-autocomplete'),
            reverse_lazy('position-add', urlconf='shastra_compedium.urls'),
            reverse_lazy('position-update',
                         urlconf='shastra_compedium.urls',
                         args=['__fk__'])),
        required=False,
        queryset=Position.objects.all())
    usage = ChoiceField(choices=(("Meaning", "Meaning"),
                                 ("Posture Description", "Posture Description")
                                 ), required=False)

    description = DescriptionChoiceField(
        required=False,
        queryset=PositionDetail.objects.filter(usage="Posture Description"),
        )

    def __init__(self, *args, **kwargs):
        super(PositionDetailEditForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            detail = kwargs.get('instance')
            self.fields[
                'description'].queryset = PositionDetail.objects.filter(
                    usage="Posture Description",
                    position=detail.position,
                    sources__in=detail.sources.all(),
                    ).exclude(pk=detail.pk)
            if self.fields['description'].queryset.count() == 0:
                self.fields['description'].widget = HiddenInput()

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
            'description',
            'dependencies',
            ]
        widgets = {
            'chapter': NumberInput(attrs={'style': 'width: 40px'}),
            'verse_start': NumberInput(attrs={'style': 'width: 55px'}),
            'verse_end': NumberInput(attrs={'style': 'width: 55px'}),
            'sources': SelectMultiple(attrs={'style': 'width: 500px'}),
            'dependencies': autocomplete.ModelSelect2Multiple(
                url='positiondetail-autocomplete',
                forward=('sources',
                         'position',
                         forward.Const('Posture Description', 'usage')))}

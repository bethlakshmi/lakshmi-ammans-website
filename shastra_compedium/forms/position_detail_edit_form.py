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
from shastra_compedium.forms.default_form_text import position_detail_help
from django.urls import reverse_lazy


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

    def is_valid(self):
        from shastra_compedium.models import UserMessage
        valid = super(PositionDetailEditForm, self).is_valid()

        if valid:
            if self.cleaned_data['description'] and self.cleaned_data[
                    'description'].sources.filter(
                        id__in=self.cleaned_data['sources']).count() == 0:
                self._errors[
                    'description'] = UserMessage.objects.get_or_create(
                        view=self.__class__.__name__,
                        code="MUST_HAVE_SAME_SOURCE",
                        defaults={
                            'summary': "Must Have the Same Source",
                            'description': position_detail_help['same_source']
                            })[0].description
                valid = False
            if self.cleaned_data['dependencies']:
                errors = []
                for dependancy in self.cleaned_data['dependencies']:
                    if dependancy.sources.filter(id__in=self.cleaned_data[
                            'sources']).count() == 0:
                        errors += [position_detail_help[
                            'same_source2'] % str(dependancy)]
                        valid = False
                if len(errors) > 0:
                    self._errors['dependencies'] = errors
        return valid

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
            'description': autocomplete.ModelSelect2(
                url='positiondetail-autocomplete',
                forward=('sources',
                         forward.Field('position', 'position_only'),
                         'id',
                         forward.Const('Posture Description', 'usage'))),
            'dependencies': autocomplete.ModelSelect2Multiple(
                url='positiondetail-autocomplete',
                forward=('sources',
                         'position',
                         forward.Const('Posture Description', 'usage')))}

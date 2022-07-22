from django.forms import (
    CheckboxSelectMultiple,
    HiddenInput,
    ModelForm,
    ModelMultipleChoiceField,
    MultipleHiddenInput,
)
from shastra_compedium.models import CombinationDetail as Combo
from shastra_compedium.models import ExampleImage
from shastra_compedium.models import PositionDetail as PosDetail
from django.utils.safestring import mark_safe
from easy_thumbnails.files import get_thumbnailer
from shastra_compedium.forms.default_form_text import item_image_help
from django.utils.html import strip_tags


class DetailsChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return mark_safe("%s: %s - %s" % (
            obj.sources.first(),
            obj.verses(),
            strip_tags(obj.contents)))


class ImageDetailForm(ModelForm):
    options = {'size': (200, 200), 'crop': False}
    required_css_class = 'required'
    error_css_class = 'error'
    details = DetailsChoiceField(
        queryset=PosDetail.objects.all(),
        widget=CheckboxSelectMultiple(attrs={'class': 'nobullet'}),
        required=False)
    combinations = DetailsChoiceField(
        queryset=Combo.objects.all(),
        widget=CheckboxSelectMultiple(attrs={'class': 'nobullet'}),
        required=False)

    def is_valid(self):
        valid = super(ImageDetailForm, self).is_valid()

        if valid:
            no_details = (not self.cleaned_data['details'] or (
                self.cleaned_data['details'].count()) == 0)
            no_combos = (not self.cleaned_data['combinations'] or (
                self.cleaned_data['combinations'].count()) == 0)

            if (not self.cleaned_data['general']) and no_details and no_combos:
                self._errors['general'] = item_image_help['general_or_details']
                valid = False
        return valid

    def __init__(self, *args, **kwargs):
        super(ImageDetailForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            instance = kwargs.get('instance')
            if instance.position:
                self.fields['details'].queryset = PosDetail.objects.filter(
                    position=instance.position)
            else:
                self.fields['details'].queryset = instance.details.all()
                self.fields['details'].widget = MultipleHiddenInput()

            if instance.subject:
                self.fields['combinations'].queryset = Combo.objects.filter(
                    subject=instance.subject)
            else:
                self.fields['combinations'].queryset = instance.details.all()
                self.fields['combinations'].widget = MultipleHiddenInput()

    class Meta:
        model = ExampleImage
        fields = [
            'id',
            'general',
            'details',
            'combinations']
        labels = {'general': "Main Image for both position and subject"}

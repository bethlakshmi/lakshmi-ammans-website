from django.forms import (
    CheckboxSelectMultiple,
    HiddenInput,
    ModelForm,
    ModelMultipleChoiceField,
    MultipleHiddenInput,
)
from shastra_compedium.models import (
    CombinationDetail,
    ExampleImage,
    PositionDetail,
)
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
        queryset=PositionDetail.objects.all(),
        widget=CheckboxSelectMultiple(attrs={'class': 'nobullet'}),
        required=False)
    combinations = DetailsChoiceField(
        queryset=CombinationDetail.objects.all(),
        widget=CheckboxSelectMultiple(attrs={'class': 'nobullet'}),
        required=False)

    def is_valid(self):
        from shastra_compedium.models import UserMessage
        valid = super(ImageDetailForm, self).is_valid()

        if valid:
            if (not self.cleaned_data['general']) and (
                    not self.cleaned_data['details']):
                self._errors['details'] = UserMessage.objects.get_or_create(
                    view="ImageDetailSet",
                    code="GENERAL_OR_DETAILS_REQUIRED",
                    defaults={
                        'summary': "Must pick general or details or both",
                        'description': item_image_help['general_or_details']
                        })[0].description
                valid = False
        return valid

    def __init__(self, *args, **kwargs):
        super(ImageDetailForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            instance = kwargs.get('instance')
            if instance.position:
                self.fields['details'].queryset = PositionDetail.objects.filter(
                    position=instance.position)
            else:
                self.fields['details'].queryset = instance.details.all()
                self.fields['details'].widget = MultipleHiddenInput()

            if instance.subject:
                self.fields['combinations'].queryset = CombinationDetail.objects.filter(
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

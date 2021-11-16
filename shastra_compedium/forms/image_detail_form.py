from django.forms import (
    CheckboxSelectMultiple,
    HiddenInput,
    ModelForm,
    ModelMultipleChoiceField,
)
from shastra_compedium.models import (
    ExampleImage,
    PositionDetail,
)
from django.utils.safestring import mark_safe
from easy_thumbnails.files import get_thumbnailer
from shastra_compedium.forms.default_form_text import item_image_help
from django.utils.html import strip_tags


class DetailsChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return mark_safe(strip_tags(obj.contents))


class ImageDetailForm(ModelForm):
    options = {'size': (200, 200), 'crop': False}
    required_css_class = 'required'
    error_css_class = 'error'
    details = DetailsChoiceField(
        queryset=PositionDetail.objects.all(),
        widget=CheckboxSelectMultiple(attrs={'class':'nobullet'}),
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
            self.fields['details'].queryset = PositionDetail.objects.filter(
                    position=instance.position)
            thumb_url = get_thumbnailer(instance.image).get_thumbnail(
                self.options).url
            self.fields['details'].label = mark_safe(
                "<img src='%s' title='%s'/><br>%s" % (
                            thumb_url,
                            instance.image,
                            instance.position.name))

    class Meta:
        model = ExampleImage
        fields = [
            'id',
            'general',
            'details']
        labels = {'general': "Main Image?"}

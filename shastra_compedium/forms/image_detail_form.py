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
from filer.models.imagemodels import Image
from django.utils.safestring import mark_safe
from easy_thumbnails.files import get_thumbnailer


class DetailsChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return mark_safe(obj.contents)


class ImageDetailForm(ModelForm):
    options = {'size': (150, 150), 'crop': False}
    required_css_class = 'required'
    error_css_class = 'error'
    details = DetailsChoiceField(queryset=PositionDetail.objects.all(),
                                 widget=CheckboxSelectMultiple)

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
            'details']

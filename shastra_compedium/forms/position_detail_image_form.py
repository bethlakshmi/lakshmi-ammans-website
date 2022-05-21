from django.forms import (
    CheckboxSelectMultiple,
    HiddenInput,
    ModelForm,
    ModelMultipleChoiceField,
)
from django.forms.widgets import CheckboxSelectMultiple
from shastra_compedium.models import (
    ExampleImage,
    PositionDetail,
)
from django.utils.safestring import mark_safe
from easy_thumbnails.files import get_thumbnailer
from shastra_compedium.forms.default_form_text import item_image_help
from django.utils.html import strip_tags
from shastra_compedium.site_text import image_modal


class ThumbnailImageField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        options = {'size': (100, 100), 'crop': False}
        thumb_url = get_thumbnailer(obj.image).get_thumbnail(options).url
        other_links = "Filename: %s" % (obj.image.original_filename)
        return mark_safe(
            "<img src='%s' title='%s'/>" % (thumb_url, other_links))


class PositionDetailImageForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'
    exampleimage_set = ThumbnailImageField(
        widget=CheckboxSelectMultiple(attrs={'class': 'nobullet'}),
        required=False,
        queryset=ExampleImage.objects.all())
    
    class Meta:
        model = PositionDetail
        fields = ['id', ]
        labels = {'general': "Main Image?"}

    def __init__(self, *args, **kwargs):
        super(PositionDetailImageForm, self).__init__(*args, **kwargs)

        # Here we fetch the currently related projects into the field,     
        # so that they will display in the form.
        if self.instance.id:
            self.fields['exampleimage_set'
                ].initial = self.instance.exampleimage_set.all(
                    ).values_list('id', flat=True)
            self.fields['exampleimage_set'
                ].queryset = ExampleImage.objects.filter(
                    position=self.instance.position)
            self.fields['exampleimage_set'].label = mark_safe(
                "<b>%s - %s - %s</b><br>%s" % (
                    self.instance.position.name,
                    self.instance.usage,
                    self.instance.verses(),
                    self.instance.contents))

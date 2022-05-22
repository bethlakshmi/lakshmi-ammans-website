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
from dal import (
    autocomplete,
    forward
)

class ThumbnailImageField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        options = {'size': (100, 100), 'crop': False}
        thumb_url = get_thumbnailer(obj.image).get_thumbnail(options).url
        other_links = "Filename: %s" % (obj.image.original_filename)
        return mark_safe(
            "<img src='%s' class='m-1' title='%s'/>" % (thumb_url, other_links))


class PositionDetailImageForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'
    exampleimage_set = ThumbnailImageField(
        widget=CheckboxSelectMultiple(attrs={'class': 'nobullet'}),
        required=False,
        queryset=ExampleImage.objects.all())

    class Meta:
        model = PositionDetail
        fields = ['id', 'dependencies']
        widgets = {
            'dependencies': autocomplete.ModelSelect2Multiple(
                attrs={'style': 'width: 100%'},
                url='positiondetail-autocomplete',
                forward=('sources',
                         'position',
                         forward.Const('Posture Description', 'usage')))}

    def __init__(self, *args, **kwargs):
        super(PositionDetailImageForm, self).__init__(*args, **kwargs)

        # Here we fetch the currently related images into the field,     
        # so that they will display in the form.  Limiting options to 
        # matched positions.
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

            options = {'size': (100, 100), 'crop': False}
            dep_label = "<b>Current Dependancies:</b><br>"
            for detail in self.instance.dependencies.all():
                for img in detail.exampleimage_set.all():
                    thumb_url = get_thumbnailer(img.image).get_thumbnail(
                        options).url
                    other_links = "Filename: %s" % (img.image.original_filename)
                    dep_label = "%s&nbsp;&nbsp;<img src='%s' title='%s'/>"% (
                        dep_label,
                        thumb_url,
                        other_links)
                dep_label = "%s<br>%s"% (dep_label, detail.contents)
            self.fields['dependencies'].label = mark_safe(dep_label) 

    def save(self, *args, **kwargs):
        instance = super(PositionDetailImageForm, self).save(*args, **kwargs)

        # Here we save the modified selection back into the database
        instance.exampleimage_set.set(self.cleaned_data['exampleimage_set'])

        return instance

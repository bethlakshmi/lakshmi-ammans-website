from django.forms import (
    CheckboxSelectMultiple,
    ModelChoiceField,
    ModelForm,
    ModelMultipleChoiceField,
)
from django.forms.widgets import RadioSelect
from shastra_compedium.models import (
    CombinationDetail,
    DanceStyle,
    ExampleImage,
    Performer,
    Position,
    PositionDetail,
    UserMessage,
)
from filer.models import Image
from shastra_compedium.forms.default_form_text import item_image_help
from dal import (
    autocomplete,
    forward
)
from django.utils.safestring import mark_safe
from easy_thumbnails.files import get_thumbnailer


class ThumbnailImageField(ModelChoiceField):
    def label_from_instance(self, obj):
        options = {'size': (200, 200), 'crop': False}
        thumb_url = get_thumbnailer(obj).get_thumbnail(options).url
        other_links = "Filename: %s" % (obj.original_filename)
        return mark_safe(
            "<img src='%s' title='%s'/>" % (thumb_url, other_links))


class ImageForm(ModelForm):
    options = {'size': (150, 150), 'crop': False}
    required_css_class = 'required'
    error_css_class = 'error'

    position = ModelChoiceField(
        queryset=Position.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(url='position-autocomplete'),
        help_text=UserMessage.objects.get_or_create(
            view="ImageUploadForm",
            code="DEFAULT_POSITION",
            defaults={
                'summary': "Default Position Help text",
                'description': item_image_help['default_position']}
            )[0].description)

    combinations = ModelMultipleChoiceField(
        queryset=CombinationDetail.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2Multiple(
            url='combination-autocomplete'),
        help_text=UserMessage.objects.get_or_create(
            view="ImageUploadForm",
            code="DEFAULT_COMBINATION",
            defaults={
                'summary': "Default Combination Help text",
                'description': item_image_help['default_combination']}
            )[0].description)

    performer = ModelChoiceField(
        queryset=Performer.objects.all(),
        required=False,
        help_text=UserMessage.objects.get_or_create(
            view="ImageUploadForm",
            code="DEFAULT_PERFORMER",
            defaults={
                'summary': "Default Performer Help text",
                'description': item_image_help['default_performer']}
            )[0].description)

    dance_style = ModelChoiceField(
        queryset=DanceStyle.objects.all(),
        required=True,
        help_text=UserMessage.objects.get_or_create(
            view="ImageUploadForm",
            code="DEFAULT_STYLE",
            defaults={
                'summary': "Default Dance Style Help text",
                'description': item_image_help['default_dance_style']}
        )[0].description)

    details = ModelMultipleChoiceField(
        queryset=PositionDetail.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(
            url='positiondetail-example-autocomplete',
            forward=(forward.Field('position', 'position_only'), )),
        required=False)

    image = ThumbnailImageField(
        widget=RadioSelect(attrs={'class': 'nobullet'}),
        queryset=Image.objects.filter(folder__name="PositionImageUploads"),
        required=True,
        empty_label=None)

    def is_valid(self):
        from shastra_compedium.models import UserMessage
        valid = super(ImageForm, self).is_valid()

        if valid:
            if (not self.cleaned_data['position']) and (
                    not self.cleaned_data['combinations']):
                self._errors['position'] = UserMessage.objects.get_or_create(
                    view="ImageForm",
                    code="POSITION_OR_COMBINATION_REQUIRED",
                    defaults={
                        'summary': "Must pick position and/or combo detail",
                        'description': item_image_help['position_or_combo']
                        })[0].description
                valid = False
            if self.cleaned_data['position'] and (
                    not self.cleaned_data['general']) and (
                    not self.cleaned_data['details']):
                self._errors['details'] = UserMessage.objects.get_or_create(
                    view="ImageForm",
                    code="GENERAL_OR_DETAILS_REQUIRED",
                    defaults={
                        'summary': "Must pick general or details or both",
                        'description': item_image_help['general_or_details']
                        })[0].description
                valid = False
            if self.cleaned_data['position'] is None and (
                    self.cleaned_data['details']):
                self._errors['position'] = UserMessage.objects.get_or_create(
                    view="ImageForm",
                    code="DETAILS_REQUIRE_POSITION",
                    defaults={
                        'summary': "Must pick a position to attach details",
                        'description': item_image_help['pos_and_details']
                        })[0].description
                valid = False
        return valid

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs.get('instance') is not None:
            self.fields['image'].queryset = Image.objects.filter(
                pk=kwargs.get('instance').image.pk)
            self.fields['details'].queryset = PositionDetail.objects.filter(
                    position=kwargs.get('instance').position)
        elif 'initial' in kwargs and 'image' in kwargs['initial']:
            self.fields['image'].queryset = Image.objects.filter(
                pk=kwargs.get('initial').get('image').pk)

    class Meta:
        model = ExampleImage
        fields = [
            'image',
            'performer',
            'dance_style',
            'combinations',
            'position',
            'general',
            'details']
        labels = {'general': "Main Image?"}

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
    Subject,
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

    subject = ModelChoiceField(
        queryset=Subject.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(url='subject-autocomplete'),
        help_text=UserMessage.objects.get_or_create(
            view="ImageUploadForm",
            code="DEFAULT_SUBJECT",
            defaults={
                'summary': "Default Subject Help text",
                'description': item_image_help['default_subject']}
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
        valid = super(ImageForm, self).is_valid()

        if valid:
            if (not self.cleaned_data['position']) and (
                    not self.cleaned_data['subject']):
                self._errors['position'] = item_image_help[
                    'position_or_subject']
                valid = False

            # Position vs. detail checks
            if self.cleaned_data['position'] is None and (
                    self.cleaned_data['details']):
                self._errors['position'] = item_image_help['pos_and_details']
                valid = False
            elif self.cleaned_data['position'] is not None:
                if not self.cleaned_data['general'] and (
                        not self.cleaned_data['details']):
                    self._errors['details'] = item_image_help[
                       'general_or_details']
                    valid = False
                else:
                    for detail in self.cleaned_data['details']:
                        if detail.position != self.cleaned_data['position']:
                            if 'details' not in self._errors:
                                self._errors['details'] = item_image_help[
                                   'pos_detail_mismatch']
                            self._errors['details'] = "%s - %s." % (
                                self._errors['details'],
                                str(detail))
                            valid = False

            # Subject vs. combo checks
            if self.cleaned_data['subject'] is None and (
                    self.cleaned_data['combinations']):
                self._errors['subject'] = item_image_help['subject_and_combos']
                valid = False
            elif self.cleaned_data['subject'] is not None:
                if not self.cleaned_data['general'] and (
                        not self.cleaned_data['combinations']):
                    self._errors['combinations'] = item_image_help[
                       'general_or_combos']
                    valid = False
                else:
                    for detail in self.cleaned_data['combinations']:
                        if detail.subject != self.cleaned_data['subject']:
                            if 'combinations' not in self._errors:
                                self._errors['combinations'] = item_image_help[
                                   'subj_comb_mismatch']
                            self._errors['combinations'] = "%s - %s." % (
                                self._errors['combinations'],
                                str(detail))
                            valid = False
        return valid

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs.get('instance') is not None:
            self.fields['image'].queryset = Image.objects.filter(
                pk=kwargs.get('instance').image.pk)

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
            'subject',
            'general',
            'details']
        labels = {'general': "Main Image?"}

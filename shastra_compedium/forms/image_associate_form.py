from django.forms import (
    HiddenInput,
    ModelForm,
    ModelChoiceField,
    ModelMultipleChoiceField,
)
from shastra_compedium.models import (
    CombinationDetail,
    ExampleImage,
    Position,
    Subject,
)
from dal import autocomplete
from filer.models.imagemodels import Image
from shastra_compedium.forms.default_form_text import item_image_help


class ImageAssociateForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'
    image = ModelChoiceField(widget=HiddenInput(),
                             queryset=Image.objects.all())
    position = ModelChoiceField(
        queryset=Position.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(url='position-autocomplete'))

    subject = ModelChoiceField(
        queryset=Subject.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(
            url='subject-autocomplete'))

    def is_valid(self):
        from shastra_compedium.models import UserMessage
        valid = super(ImageAssociateForm, self).is_valid()

        if valid:
            if (not self.cleaned_data['position']) and (
                    not self.cleaned_data['subject']):
                self._errors['position'] = UserMessage.objects.get_or_create(
                    view="BulkImageUpload",
                    code="POSITION_OR_SUBJECT_REQUIRED",
                    defaults={
                        'summary': "Must pick position and/or subject",
                        'description': item_image_help['position_or_subject']
                        })[0].description
                valid = False
        return valid

    class Meta:
        model = ExampleImage
        fields = [
            'image',
            'position',
            'subject',
            'performer',
            'dance_style']

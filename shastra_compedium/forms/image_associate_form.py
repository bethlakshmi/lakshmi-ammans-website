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

    combinations = ModelMultipleChoiceField(
        queryset=CombinationDetail.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2Multiple(
            url='combination-autocomplete'))

    def is_valid(self):
        from shastra_compedium.models import UserMessage
        valid = super(ImageAssociateForm, self).is_valid()

        if valid:
            if (not self.cleaned_data['position']) and (
                    not self.cleaned_data['combinations']):
                self._errors['position'] = UserMessage.objects.get_or_create(
                    view="BulkImageUpload",
                    code="POSITION_OR_COMBINATION_REQUIRED",
                    defaults={
                        'summary': "Must pick position and/or combo detail",
                        'description': item_image_help['position_or_combo']
                        })[0].description
                valid = False
        return valid

    class Meta:
        model = ExampleImage
        fields = [
            'image',
            'position',
            'combinations',
            'performer',
            'dance_style']

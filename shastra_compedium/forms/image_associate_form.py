from django.forms import (
    CharField,
    HiddenInput,
    ModelForm,
    ModelChoiceField,
)
from shastra_compedium.models import (
    ExampleImage,
    Position,
)
from dal import autocomplete
from filer.models.imagemodels import Image


class ImageAssociateForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'
    image = ModelChoiceField(widget=HiddenInput(),queryset=Image.objects.all())
    position = ModelChoiceField(
        queryset=Position.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(url='position-autocomplete'))

    class Meta:
        model = ExampleImage
        fields = [
            'image',
            'position',
            'details',
            'performer',
            'dance_style']

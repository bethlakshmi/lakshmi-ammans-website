from django.forms import (
    ClearableFileInput,
    ImageField,
    IntegerField,
    Form,
    HiddenInput,
    ModelChoiceField,
)
from shastra_compedium.models import (
    DanceStyle,
    Performer,
    UserMessage,
)
from filer.models import Image
from shastra_compedium.forms.default_form_text import item_image_help


class ImageUploadForm(Form):
    required_css_class = 'required'
    error_css_class = 'error'

    default_performer = ModelChoiceField(
        queryset=Performer.objects.all(),
        required=False,
        help_text=UserMessage.objects.get_or_create(
            view="ImageUploadForm",
            code="DEFAULT_PERFORMER",
            defaults={
                'summary': "Default Performer Help text",
                'description': item_image_help['default_performer']}
            )[0].description)
    default_dance_style = ModelChoiceField(
        queryset=DanceStyle.objects.all(),
        required=True,
        help_text=UserMessage.objects.get_or_create(
            view="ImageUploadForm",
            code="DEFAULT_PERFORMER",
            defaults={
                'summary': "Default Performer Help text",
                'description': item_image_help['default_dance_style']}
        )[0].description)
    new_images = ImageField(
        widget=ClearableFileInput(attrs={'multiple': True}),
        required=True,
        help_text=UserMessage.objects.get_or_create(
                view="ImageUploadForm",
                code="NEW_IMAGE_INSTRUCTIONS",
                defaults={
                    'summary': "New Image Help text",
                    'description': item_image_help['new_images']}
                )[0].description)

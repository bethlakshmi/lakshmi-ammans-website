from django.forms import (
    CharField,
    ImageField,
    ModelForm,
    SelectMultiple,
    Textarea,
)
from shastra_compedium.models import Performer
from django_addanother.widgets import AddAnotherEditSelectedWidgetWrapper
from django.urls import reverse_lazy


class PerformerForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'
    linneage = CharField(
        widget=Textarea(attrs={'class': 'admin-tiny-mce'}),
        initial=" ")
    bio = CharField(
        widget=Textarea(attrs={'class': 'admin-tiny-mce'}),
        initial=" ")

    class Meta:
        model = Performer
        fields = ['name',
                  'linneage',
                  'dance_styles',
                  'bio',
                  'contact',
                  'image']
        help_texts = {
            'linneage': '''Please describe the history of the teachers the
                 performer has studied with.'''}
        widgets = {
            'dance_styles': AddAnotherEditSelectedWidgetWrapper(
                SelectMultiple,
                reverse_lazy('dancestyle-add', urlconf='shastra_compedium.urls'),
                reverse_lazy('dancestyle-update',
                             urlconf='shastra_compedium.urls',
                             args=['__fk__'])),
            }

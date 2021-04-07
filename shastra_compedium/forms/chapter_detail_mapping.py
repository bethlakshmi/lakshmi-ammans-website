from django.forms import (
    ChoiceField,
    Form,
    HiddenInput,
    IntegerField,
    ModelChoiceField,
)
from shastra_compedium.models import Category


class ChapterDetailMapping(Form):
    required_css_class = 'required'
    error_css_class = 'error'
    step = IntegerField(widget=HiddenInput(), initial=1)
    num_rows = IntegerField(widget=HiddenInput(), required=True)

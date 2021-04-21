from django.forms import (
    ModelForm,
    Select,
)
from shastra_compedium.models import Position
from django_addanother.widgets import AddAnotherEditSelectedWidgetWrapper
from django.urls import reverse_lazy


class PositionForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'

    class Meta:
        model = Position
        fields = ['name', 'category', 'order']
        widgets = {
            'category': AddAnotherEditSelectedWidgetWrapper(
                Select,
                reverse_lazy('category-add', urlconf='shastra_compedium.urls'),
                reverse_lazy('category-update',
                             urlconf='shastra_compedium.urls',
                             args=['__fk__'])),
            }

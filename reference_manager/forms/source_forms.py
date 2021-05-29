from django.forms import (
    ModelMultipleChoiceField,
    ModelForm,
    SelectMultiple,
)
from django.urls import reverse_lazy
from django_addanother.widgets import AddAnotherWidgetWrapper
from reference_manager.models import (
    Category,
    URLSource,
)


class URLSourceForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'


    class Meta:
        model = URLSource
        fields = ['name', 'description', 'location']

    def __init__(self, *args, **kwargs):
        super(URLSourceForm, self).__init__(*args, **kwargs)

        if 'instance' in kwargs:
            instance = kwargs.get('instance')

        for category in Category.objects.all():
            self.fields['cat_%d' % category.pk] = ModelMultipleChoiceField(
                widget=AddAnotherWidgetWrapper(
                    SelectMultiple,
                    reverse_lazy('tag-add',
                                 urlconf='reference_manager.urls',
                                 args=[category.pk])),
                queryset=category.tag_set,
                label=category.name,
                help_text=category.instructions)


'''
    def save(self, commit=True):
        style_value = super(StyleValueForm, self).save(commit=False)
        i = 0
        value = ""
        for template in style_value.style_property.value_type.split():
            if template == "rgba":
                value = value + self.cleaned_data['value_%d' % i] + " "
            elif template == "px":
                value = value + str(self.cleaned_data['value_%d' % i]) + "px "
            i = i + 1
        style_value.value = value.strip()
        if commit:
            style_value.save()
        return style_value
'''

from django.views.generic.edit import CreateView, UpdateView
from django_addanother.views import CreatePopupMixin, UpdatePopupMixin
from shastra_compedium.models import ExampleImage
from django.urls import reverse_lazy
from shastra_compedium.site_text import make_example_image_messages
from shastra_compedium.views import ShastraFormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from shastra_compedium.forms import (CopyImageForm,
                                     ImageForm)
from filer.models.imagemodels import Image


class ExampleImageMixin(ShastraFormMixin):
    def get_success_url(self):
        return "%s?changed_ids=%s&obj_type=%s" % (
            self.request.GET.get('next', self.success_url),
            str([self.object.image.pk]),
            self.object.__class__.__name__)

class ExampleImageUpdate(LoginRequiredMixin,
                         UpdatePopupMixin,
                         ExampleImageMixin,
                         UpdateView):
    model = ExampleImage
    template_name = 'shastra_compedium/modal_make_form.tmpl'
    success_url = reverse_lazy('image_list',
                               urlconf="shastra_compedium.urls")
    page_title = 'Example Image'
    view_title = 'Update Example Image'
    valid_message = make_example_image_messages['edit_success']
    intro_message = make_example_image_messages['edit_intro']
    form_class = ImageForm


class ExampleImageCreate(LoginRequiredMixin,
                         CreatePopupMixin,
                         ExampleImageMixin,
                         CreateView):
    model = ExampleImage
    template_name = 'shastra_compedium/modal_make_form.tmpl'
    success_url = reverse_lazy('image_list',
                               urlconf="shastra_compedium.urls")
    page_title = 'Example Image'
    view_title = 'Create Example Image'
    valid_message = make_example_image_messages['create_success']
    intro_message = make_example_image_messages['create_intro']
    form_class = ImageForm

    def get_initial(self):
        initial = super().get_initial()
        initial['image'] = Image.objects.get(pk=self.kwargs['image_id'])
        return initial

class ExampleImageCopy(LoginRequiredMixin,
                       CreatePopupMixin,
                       ExampleImageMixin,
                       CreateView):
    model = ExampleImage
    template_name = 'shastra_compedium/modal_make_form.tmpl'
    success_url = reverse_lazy('image_list',
                               urlconf="shastra_compedium.urls")
    page_title = 'Example Image'
    view_title = 'Copy Image to a New Position'
    valid_message = make_example_image_messages['copy_success']
    intro_message = make_example_image_messages['copy_intro']
    form_class = CopyImageForm

    def get_initial(self):
        initial = super().get_initial()
        initial_example_image = ExampleImage.objects.get(
            pk=self.kwargs['image_id'])
        initial['image'] = initial_example_image.image
        initial['performer'] = initial_example_image.performer
        initial['dance_style'] = initial_example_image.dance_style
        return initial

from shastra_compedium.views import GenericWizard
from shastra_compedium.forms import (
    ImageDetailForm,
    ImageUploadForm,
    ImageAssociateForm,
    ImageAssociateMetaForm,
)
from shastra_compedium.models import ExampleImage
from django.contrib import messages
from shastra_compedium.functions import upload_and_attach
from django.utils.safestring import mark_safe
from easy_thumbnails.files import get_thumbnailer
from django.forms import modelformset_factory
from django.urls import reverse
from shastra_compedium.site_text import image_modal
from filer.models.imagemodels import Image


class BulkImageUpload(GenericWizard):
    filer_images = []
    template = 'shastra_compedium/bulk_image_wizard.tmpl'
    page_title = 'Image Upload'
    first_title = 'Select Images to Upload'
    second_title = 'Connect Images to Positions'
    third_title = 'Set Specific Details'
    form_sets = {
        -1: {
            'the_form':  None,
            'next_form': ImageUploadForm,
            'next_title': first_title},
        0: {
            'the_form':  ImageUploadForm,
            'next_form': ImageAssociateForm,
            'next_title': second_title,
            'instruction_key': "IMAGE_CONNECT_INTRO"},
        1: {
            'the_form':  ImageAssociateForm,
            'next_form': ImageDetailForm,
            'next_title': third_title},
        2: {
            'the_form': ImageDetailForm,
            'is_formset': True,
            'next_form': None,
            'next_title': None},
    }
    options = {'size': (100, 100), 'crop': False}
    changed_ids = []

    def finish_valid_form(self, request):
        self.changed_ids = []
        files = request.FILES.getlist('new_images')
        if len(files) > 0:
            self.num_files = len(files)
            self.filer_images = upload_and_attach(
                files,
                request.user)
        elif self.forms[0].__class__.__name__ == "ImageAssociateForm":
            for form in self.forms:
                if form.__class__.__name__ == "ImageAssociateForm":
                    pk = form.save().pk
                    self.changed_ids += [pk]
        else:
            self.forms.save()
            self.num_files = self.forms.total_form_count()
            for changed_object, changed_fields in self.forms.changed_objects:
                self.changed_ids += [changed_object.pk]

    def finish(self, request):
        return_url = reverse('image_list', urlconf='shastra_compedium.urls')
        messages.success(
            request,
            "Uploaded %d images." % (self.num_files))
        if len(self.changed_ids) > 0:
            return_url = "%s?changed_ids=%s&obj_type=ExampleImage" % (
                return_url,
                str(self.changed_ids))
        return return_url

    def setup_forms(self, form, request=None):
        if request:
            if str(form().__class__.__name__) == "ImageUploadForm":
                return [form(request.POST, request.FILES)]
            elif str(form().__class__.__name__) == "ImageAssociateForm":
                meta_form = ImageAssociateMetaForm(request.POST)
                if not meta_form.is_valid():
                    return []
                self.num_files = meta_form.cleaned_data['association_count']
                forms = []
                for i in range(0, self.num_files):
                    association_form = form(request.POST,
                                            prefix=str(i),
                                            label_suffix='')
                    if association_form.is_valid():
                        image = association_form.cleaned_data['image']
                    else:
                        image = Image.objects.filter(
                            pk=request.POST["%d-image" % i]).first()
                    if image is not None:
                        thumb_url = get_thumbnailer(image).get_thumbnail(
                            self.options).url
                        association_form.fields['position'].label = mark_safe(
                            image_modal % (image.pk,
                                           thumb_url,
                                           image,
                                           image.pk,
                                           image.url))
                    forms += [association_form]
                forms += [meta_form]
                return forms
            else:
                ImageDetailFormSet = modelformset_factory(ExampleImage,
                                                          form=ImageDetailForm,
                                                          extra=0)
                forms = ImageDetailFormSet(request.POST)
                return forms

        else:
            if str(form().__class__.__name__) == "ImageUploadForm":
                return [form()]
            elif str(form().__class__.__name__) == "ImageAssociateForm":
                forms = []
                association_num = 0
                for image in self.filer_images:
                    association_form = form(
                        initial={
                            'image': image,
                            'dance_style': self.forms[0].cleaned_data[
                                'default_dance_style'],
                            'performer': self.forms[0].cleaned_data[
                                'default_performer']},
                        prefix=str(association_num),
                        label_suffix='')
                    thumb_url = get_thumbnailer(image).get_thumbnail(
                        self.options).url
                    association_form.fields['position'].label = mark_safe(
                        image_modal % (image.pk,
                                       thumb_url,
                                       image,
                                       image.pk,
                                       image.url))
                    forms += [association_form]
                    association_num = association_num + 1
                forms += [ImageAssociateMetaForm(
                    initial={'association_count': association_num})]
                return forms
            else:
                ImageDetailFormSet = modelformset_factory(ExampleImage,
                                                          form=ImageDetailForm,
                                                          extra=0)
                forms = ImageDetailFormSet(
                    queryset=ExampleImage.objects.filter(
                        pk__in=self.changed_ids))
                return forms

    def make_context(self, request, valid=True):
        context = super(BulkImageUpload, self).make_context(request, valid)
        if str(self.forms[0].__class__.__name__) == "ImageAssociateForm":
            context['special_handling'] = True
        elif str(self.forms.__class__.__name__) == "ExampleImageFormFormSet":
            context['special_handling'] = True
            self.template = 'shastra_compedium/bulk_image_wizard2.tmpl'
        return context

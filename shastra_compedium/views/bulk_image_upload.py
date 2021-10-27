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


class BulkImageUpload(GenericWizard):
    filer_images = []
    example_images = []
    template = 'shastra_compedium/bulk_image_wizard.tmpl'
    page_title = 'Image Upload'
    first_title = 'Select Images to Upload'
    second_title = 'Connect Images to Positions'
    third_title = 'Set Specific Position Details'
    form_sets = {
        -1: {
            'the_form':  None,
            'next_form': ImageUploadForm,
            'next_title': first_title},
        0: {
            'the_form':  ImageUploadForm,
            'next_form': ImageAssociateForm,
            'next_title': second_title},
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

    def finish_valid_form(self, request):
        files = request.FILES.getlist('new_images')
        self.example_images = []
        if len(files) > 0:
            self.num_files = len(files)
            self.filer_images = upload_and_attach(
                files,
                request.user)
        elif self.forms[0].__class__.__name__ == "ImageAssociateForm" or (
                self.forms[0].__class__.__name__ == "ImageDetailForm"):
            for form in self.forms:
                if form.__class__.__name__ == "ImageAssociateForm" and (
                        form.cleaned_data['position']):
                    self.example_images += [form.save().pk]
                elif form.__class__.__name__ == "ImageDetailForm":
                    self.example_images += [form.save().pk]
        else:
            self.forms.save()

    def finish(self, request):
        messages.success(
            request,
            "Uploaded %s images.<br>Attached %s images." % (
                self.num_files,
                len(self.example_images)))
        return self.return_url

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
                        thumb_url = get_thumbnailer(image).get_thumbnail(
                            self.options).url
                        association_form.fields['position'].label = mark_safe(
                            "<img src='%s' title='%s'/>" % (thumb_url, image))
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
                                'default_performer'],},
                        prefix=str(association_num),
                        label_suffix='')
                    thumb_url = get_thumbnailer(image).get_thumbnail(
                        self.options).url
                    association_form.fields['position'].label = mark_safe(
                        "<img src='%s' title='%s'/>" % (thumb_url, image))
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
                        pk__in=self.example_images))
                return forms

    def make_context(self, request):
        context = super(BulkImageUpload, self).make_context(request)
        if str(self.forms[0].__class__.__name__) == "ImageAssociateForm":
            context['special_handling'] = True
        elif str(self.forms.__class__.__name__) == "ExampleImageFormFormSet":
            context['special_handling'] = True
            self.template = 'shastra_compedium/bulk_image_wizard2.tmpl'
        return context

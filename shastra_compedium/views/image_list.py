from shastra_compedium.views import GenericList
from shastra_compedium.models import ExampleImage
from filer.models.imagemodels import Image
from django.utils.safestring import mark_safe


class ImageList(GenericList):
    template = 'shastra_compedium/image_list.tmpl'
    title = "List of Images"

    def get_context_dict(self):
        context = super(ImageList, self).get_context_dict()
        if self.changed_obj != "ExampleImage":
            context['changed_ids'] = []
        else:
            changed_ids = []
            for i in ExampleImage.objects.filter(
                    pk__in=self.changed_ids).values_list('image__pk',
                                                         flat=True):
                changed_ids += [i]
            context['changed_ids'] = changed_ids
        return context

    def get_list(self):
        example_dict = {}
        for example in ExampleImage.objects.all():
            if example.image in example_dict:
                example_dict[example.image] += [example]
            else:
                example_dict[example.image] = [example]
        return {"exampleimages": example_dict,
                "images": Image.objects.filter(
                    folder__name="PositionImageUploads",
                    exampleimage__isnull=True)}

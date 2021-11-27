from shastra_compedium.views import GenericList
from shastra_compedium.models import ExampleImage


class ImageList(GenericList):
    template = 'shastra_compedium/image_list.tmpl'
    title = "List of Images"

    def get_context_dict(self):
        context = super(ImageList, self).get_context_dict()
        if self.changed_obj != "ExampleImage":
            context['changed_ids'] = []
        return context

    def get_list(self):
        return {"exampleimages": ExampleImage.objects.all()}

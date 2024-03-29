from shastra_compedium.models import (
    ExampleImage,
    PositionDetail,
    Position,
    Shastra,
    Source,
)
from shastra_compedium.views import GenericList
from django.db.models import Count


class PositionList(GenericList):
    template = 'shastra_compedium/position_list.tmpl'
    title = "List of Positions"

    def get_context_dict(self):
        context = super(PositionList, self).get_context_dict()
        context['sources'] = Source.objects.all()
        context['shastras'] = Shastra.objects.all()
        if self.changed_obj == "Category":
            context['category_ids'] = context['changed_ids']
            context['changed_ids'] = []
        elif self.changed_obj != "Position":
            context['changed_ids'] = []
        return context

    def get_list(self):
        details = {}
        for detail in PositionDetail.objects.filter(description__isnull=True):
            if detail.position not in details:
                details[detail.position] = {"images": [],
                                            "sources": {}}
            for source in detail.sources.all():
                usage = detail.usage.replace(" ", "")
                if source not in details[detail.position]["sources"]:
                    details[detail.position]["sources"][source] = {
                        usage: [detail],
                        'num_details': 0}
                elif usage not in details[detail.position]["sources"][source]:
                    details[detail.position]["sources"][source][usage] = [
                        detail]
                else:
                    details[detail.position]["sources"][source][usage] += [
                        detail]
                details[detail.position]["sources"][source][
                    'num_details'] = details[
                        detail.position]["sources"][source]['num_details'] + 1
        for image in ExampleImage.objects.filter(general=True):
            if image.position in details:
                details[image.position]["images"] += [image]
            else:
                details[image.position] = {"images": [image]}
        for position in Position.objects.all().annotate(img_count=Count(
                'exampleimage')):
            if position not in details:
                details[position] = {"image_total": position.img_count}
            else:
                details[position]["image_total"] = position.img_count
        return details

from shastra_compedium.views import GenericList
from shastra_compedium.models import (
    CombinationDetail,
    ExampleImage,
)


class CombinationList(GenericList):
    template = 'shastra_compedium/combination_list.tmpl'
    title = "List of Combinations"

    def get_context_dict(self):
        context = super(CombinationList, self).get_context_dict()
        if self.changed_obj != "CombinationDetail":
            context['changed_ids'] = []
        return context

    def get_list(self):
        subject_dict = {}
        for detail in CombinationDetail.objects.all():
            key = "NONE"

            if detail.subject is not None:
                key = detail.subject
            if key in subject_dict:
                subject_dict[key]['combos'] += [detail]
            else:
                subject_dict[key] = {'combos': [detail],
                                     'images': [],
                                     'subimage_count': 0,
                                     'sources': []}

            subject_dict[key]['subimage_count'] = subject_dict[key][
                'subimage_count'] + detail.exampleimage_set.all().count()

            for source in detail.sources.all():
                if source not in subject_dict[key]['sources']:
                    subject_dict[key]['sources'] += [source]
        for image in ExampleImage.objects.filter(general=True,
                                                 subject__isnull=False):
            if image.subject in subject_dict:
                subject_dict[image.subject]["images"] += [image]
            else:
                subject_dict[image.subject] = {
                    "combos": [],
                    "images": [image],
                    'subimage_count': 0,
                    'sources': []}
            subject_dict[key]['subimage_count'] = subject_dict[key][
                'subimage_count'] + 1
        return {"combinations": subject_dict}

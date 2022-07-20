from shastra_compedium.views import GenericList
from shastra_compedium.models import CombinationDetail


class CombinationList(GenericList):
    template = 'shastra_compedium/combination_list.tmpl'
    title = "List of Combinations"

    def get_context_dict(self):
        context = super(CombinationList, self).get_context_dict()
        if self.changed_obj != "CombinationDetail":
            context['changed_ids'] = []
        return context

    def get_list(self):
        subject_dict  = {}
        for detail in CombinationDetail.objects.all():
            key = "NONE"

            if detail.subject is not None:
                key = detail.subject
            if key in subject_dict:
                subject_dict[key]['combos'] += [detail]
            else:
                subject_dict[key] = {'combos': [detail],
                                     'images': [],
                                     'sources': []}

            for image in detail.exampleimage_set.all():
                if image not in subject_dict[key]['images']:
                    subject_dict[key]['images'] += [image]
            for source in detail.sources.all():
                if source not in subject_dict[key]['sources']:
                    subject_dict[key]['sources'] += [source]

        return {"combinations": subject_dict}

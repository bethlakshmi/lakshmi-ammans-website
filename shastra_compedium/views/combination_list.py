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
        return {"combinations": CombinationDetail.objects.all()}

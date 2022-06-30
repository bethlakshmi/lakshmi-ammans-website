from shastra_compedium.forms import (
    ChapterForm,
    ChapterDetailMapping,
    CombinationDetailForm,
)
from shastra_compedium.views import UploadChapter
import re
from django.urls import reverse_lazy


class UploadCombination(UploadChapter):
    template = 'shastra_compedium/bulk_combo_edit.tmpl'
    page_title = 'Upload Combinations'
    first_title = 'Upload Combinations - Setup'
    second_title = 'Upload Combinations - Edit Detail Entries'
    form_sets = {
        -1: {
            'the_form':  None,
            'next_form': ChapterForm,
            'next_title': first_title,
            'instruction_key': "COMBINATION_BASICS_INTRO"},
        0: {
            'the_form':  ChapterForm,
            'next_form': ChapterDetailMapping,
            'next_title': second_title,
            'instruction_key': "COMBINATION_DETAIL_INTRO"},
        1: {
            'the_form':  ChapterDetailMapping,
            'next_form': None,
            'next_title': None},
    }
    detail_form = CombinationDetailForm
    return_url = reverse_lazy('combo_list',
                              urlconf="shastra_compedium.urls")
    obj_type = "CombinationDetail"

    def finish_valid_form(self, request):
        self.changed_ids = []
        if self.forms[0].__class__.__name__ == "ChapterForm":
            self.chapter = self.forms[0].save()
            self.chapter_positions = []
            entries = self.forms[0].cleaned_data['position_text'].split('|||')
            for entry in entries:
                chapter_pos = {}
                # sort out verse numbers
                match = re.search(
                    '(?P<verse_start>\d+)-?(?P<verse_end>\d*)(?P<text>\D+)',
                    entry)
                if match:
                    chapter_pos = match.groupdict()
                else:
                    chapter_pos = {'text': entry}

                chapter_pos['contents'] = chapter_pos['text'].strip()
                chapter_pos['chapter'] = self.chapter.chapter
                chapter_pos['sources'] = self.chapter.sources.all(
                    ).values_list('pk', flat=True)
                chapter_pos['usage'] = self.chapter.usage
                self.chapter_positions += [chapter_pos]
        else:
            self.num_created = 0
            for form in self.forms[1:]:
                if form.cleaned_data['positions']:
                    position_detail = form.save(commit=False)
                    if len(form.cleaned_data['contents'].strip()) > 0:
                        position_detail = form.save()
                        self.num_created = self.num_created + 1
                        self.changed_ids += [position_detail.pk]

    def detail_form_config(self, form, i):
        # this is simpler than chapter, we won't do add another features
        return form

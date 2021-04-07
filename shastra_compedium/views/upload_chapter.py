from shastra_compedium.forms import (
    ChapterForm,
    ChapterDetailMapping,
    PositionDetailForm,
)
from shastra_compedium.models import CategoryDetail
from shastra_compedium.views import GenericWizard
import re
from django.urls import reverse
from django.contrib import messages


class UploadChapter(GenericWizard):
    template = 'shastra_compedium/bulk_position_edit.tmpl'
    success_url = '/'
    page_title = 'Upload Chapter'
    first_title = 'Upload Chapter - Setup Chapter'
    second_title = 'Upload Chapter - Edit Detail Entries'
    form_sets = {
        -1: {
            'the_form':  None,
            'next_form': ChapterForm,
            'next_title': first_title,
            'instruction_key': "CHAPTER_BASICS_INTRO"},
        0: {
            'the_form':  ChapterForm,
            'next_form': ChapterDetailMapping,
            'next_title': second_title,
            'instruction_key': "CHAPTER_DETAIL_INTRO"},
        1: {
            'the_form':  ChapterDetailMapping,
            'next_form': None,
            'next_title': None},
    }
    header = None

    def finish_valid_form(self, request):
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
                # check for usage separators
                match_text = chapter_pos['text'].replace(
                    '\n',
                    ' ').replace('\r', '').split('(Uses)')
                if len(match_text) > 1:
                    chapter_pos['posture'] = match_text[0].strip()
                    chapter_pos['contents'] = match_text[1].strip()
                else:
                    chapter_pos['contents'] = chapter_pos['text'].strip()
                chapter_pos['chapter'] = self.chapter.chapter
                chapter_pos['usage'] = "Meaning"
                self.chapter_positions += [chapter_pos]
        else:
            self.num_created = 0
            for form in self.forms[1:]:
                position_detail = form.save(commit=False)
                if len(form.cleaned_data['contents'].strip()) > 0:
                    position_detail.save()
                    self.num_created = self.num_created + 1
                if len(form.cleaned_data['posture']) > 0:
                    position_detail.pk = None
                    position_detail.contents = form.cleaned_data['posture']
                    position_detail.usage = "Posture Description"
                    position_detail.save()
                    self.num_created = self.num_created + 1

    def finish(self, request):
        messages.success(
            request,
            "Uploaded %s position details." % (
                self.num_created))
        return self.return_url

    def make_context(self, request):
        context = super(UploadChapter, self).make_context(request)
        if str(self.forms[0].__class__.__name__) == "ChapterDetailMapping":
            context['special_handling'] = True
            context['tiny_mce_width'] = 400
        elif str(self.forms[0].__class__.__name__) == "ChapterForm":
            context['show_finish'] = False
        return context

    def setup_forms(self, form, request=None):
        if request:
            if str(form().__class__.__name__) == "ChapterForm":
                return [form(request.POST)]
            else:
                if 'num_rows' not in request.POST.keys():
                    return []
                num_rows = int(request.POST['num_rows'])
                forms = [ChapterDetailMapping(request.POST)]
                i = 0
                while i < num_rows:
                    forms += [PositionDetailForm(request.POST,
                                                 prefix=str(i))]
                    i = i + 1
                return forms
        else:
            if str(form().__class__.__name__) == "ChapterForm":
                return [form()]
            else:
                # set up the choice form based on number of columns.
                forms = [ChapterDetailMapping(initial={
                    'num_rows': len(self.chapter_positions)})]
                i = 0
                for position in self.chapter_positions:
                    form = PositionDetailForm(prefix=str(i), initial=position)
                    form.fields['position'].widget.add_related_url = reverse(
                        'position-add',
                        urlconf='shastra_compedium.urls',
                        args=[i*5, self.chapter.category.pk])
                    forms += [form]
                    i = i + 1
                return forms

from shastra_compedium.forms import (
    ChapterForm,
    ChapterDetailMapping,
    PositionDetailForm,
)
from shastra_compedium.models import (
    CategoryDetail,
    PositionDetail,
)
from shastra_compedium.views import GenericWizard
import re
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404


class UploadChapter(GenericWizard):
    template = 'shastra_compedium/bulk_position_edit.tmpl'
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
    changed_ids = []
    detail_form = PositionDetailForm

    def groundwork(self, request, args, kwargs):
        redirect = super(UploadChapter, self).groundwork(request, args, kwargs)
        self.category = None
        if "category_id" in kwargs:
            category_id = kwargs.get("category_id")
            self.category = get_object_or_404(CategoryDetail, id=category_id)

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
                # check for usage separators
                match_text = chapter_pos['text'].replace(
                    '\n',
                    ' ').replace('\r', '').split('(Uses)')
                if len(match_text) > 1:
                    chapter_pos['contents'] = match_text[0].strip()
                    chapter_pos['meaning'] = match_text[1].strip()
                else:
                    chapter_pos['meaning'] = chapter_pos['text'].strip()
                chapter_pos['chapter'] = self.chapter.chapter
                chapter_pos['sources'] = self.chapter.sources.all(
                    ).values_list('pk', flat=True)
                chapter_pos['usage'] = "Posture Description"
                self.chapter_positions += [chapter_pos]
        else:
            self.num_created = 0
            for form in self.forms[1:]:
                if form.cleaned_data['position']:
                    position_detail = form.save(commit=False)
                    posture_pk = None
                    if len(form.cleaned_data['contents'].strip()) > 0:
                        position_detail = form.save()
                        self.num_created = self.num_created + 1
                        self.changed_ids += [position_detail.position.pk]
                        posture_pk = position_detail.pk
                    if len(form.cleaned_data['meaning']) > 0:
                        position_detail.pk = None
                        position_detail.contents = form.cleaned_data['meaning']
                        position_detail.usage = "Meaning"
                        if posture_pk is not None:
                            position_detail.description = PositionDetail.objects.get(
                                pk=posture_pk)
                        position_detail.save()
                        form.save_m2m()
                        self.num_created = self.num_created + 1
                        self.changed_ids += [position_detail.position.pk]

    def finish(self, request):
        return_url = self.return_url
        if self.forms[0].__class__.__name__ == "ChapterForm":
            messages.success(
                request,
                "Uploaded chapter details - %s" % (self.chapter))
        else:
            messages.success(
                request,
                "Uploaded %s details." % (self.num_created))
        if len(self.changed_ids) > 0:
            return_url = "%s?changed_ids=%s&obj_type=Position" % (
                self.return_url,
                str(self.changed_ids))
        return return_url

    def make_context(self, request, valid=True):
        context = super(UploadChapter, self).make_context(request, valid)
        if str(self.forms[0].__class__.__name__) == "ChapterDetailMapping":
            context['special_handling'] = True
            context['tiny_mce_width'] = 400
        return context

    def setup_forms(self, form, request=None):
        if request:
            if str(form().__class__.__name__) == "ChapterForm":
                return [form(request.POST, instance=self.category)]
            else:
                if 'num_rows' not in request.POST.keys():
                    return []
                num_rows = int(request.POST['num_rows'])
                forms = [ChapterDetailMapping(request.POST)]
                i = 0
                while i < num_rows:
                    forms += [self.detail_form(request.POST, prefix=str(i))]
                    i = i + 1
                return forms
        else:
            if str(form().__class__.__name__) == "ChapterForm":
                return [form(instance=self.category)]
            else:
                # set up the choice form based on number of columns.
                forms = [ChapterDetailMapping(initial={
                    'num_rows': len(self.chapter_positions)})]
                i = 0
                for position in self.chapter_positions:
                    form = self.detail_form(prefix=str(i), initial=position)
                    forms += [self.detail_form_config(form, i)]
                    i = i + 1
                return forms

    def detail_form_config(self, form, i):
        form.fields['position'].widget.add_related_url = reverse(
            'position-add',
            urlconf='shastra_compedium.urls',
            args=[i*5, self.chapter.category.pk])
        return form

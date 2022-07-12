from django.views.generic import View
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from shastra_compedium.forms import StepForm
from shastra_compedium.models import UserMessage
from shastra_compedium.site_text import user_messages
from django.shortcuts import render


class GenericWizard(View):
    ##############
    #  This is an abstract class, it gives the logic for rolling through
    #  a set of forms as a wizard, to use it:
    #     - instantiate form_sets = a dict of integers (-1 to however many)
    #          - with a sub-dict with a "the_form", "next_form", "next_title"
    #          - there must be a -1 with the_form = None
    #          - there must be a last item with next_form and next_title
    #            as None
    #     - create setup_forms - which can make any form in the set, the first
    #          form can be  made via either get or post, all forms after that
    #          are submitted as posts.
    #     - finish_valid_form - what to do when a form is deemed valid, return
    #          True if you want to finish (out of sequence)
    #     - finish - place to put any messaging and return a URL for how to
    #          return to a main spot
    ##############
    step = -1
    max = 1
    return_url = reverse_lazy('position_list',
                              urlconf="shastra_compedium.urls")

    def groundwork(self, request, args, kwargs):
        self.step = int(request.POST.get("step", -1))

    def make_context(self, request, valid=True):
        context = {
            'page_title': self.page_title,
            'title': self.page_title,
            'subtitle': self.current_form_set['next_title'],
            'forms': self.forms,
            'show_finish': True,
            'last': self.form_sets[self.step+1]['next_form'] is None,
            'step_form': StepForm(initial={"step": self.step + 1})
        }
        if 'instruction_key' in self.current_form_set:
            context['instructions'] = UserMessage.objects.get_or_create(
                view=self.__class__.__name__,
                code=self.current_form_set['instruction_key'],
                defaults={
                    'summary': user_messages[self.current_form_set[
                        'instruction_key']]['summary'],
                    'description': user_messages[self.current_form_set[
                        'instruction_key']]['description']}
                )[0].description
        context['form_error'] = not valid
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GenericWizard, self).dispatch(*args, **kwargs)

    @never_cache
    def get(self, request, *args, **kwargs):
        redirect = self.groundwork(request, args, kwargs)
        self.current_form_set = self.form_sets[-1]
        self.forms = self.setup_forms(self.current_form_set['next_form'])
        return render(request, self.template, self.make_context(request))

    def return_on_error(self, request, message_code, extra_message=""):
        msg = UserMessage.objects.get_or_create(
                view=self.__class__.__name__,
                code=message_code,
                defaults={
                    'summary': user_messages[message_code]['summary'],
                    'description': user_messages[message_code]['description']}
                )
        messages.error(request, msg[0].description + extra_message)
        return HttpResponseRedirect(self.return_url)

    def validate_forms(self):
        all_valid = True
        if "is_formset" in self.current_form_set and (
                self.current_form_set['is_formset']):
            all_valid = self.forms.is_valid()
        else:
            for form in self.forms:
                all_valid = form.is_valid() and all_valid
        return all_valid

    @never_cache
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.groundwork(request, args, kwargs)
        if 'cancel' in list(request.POST.keys()):
            messages.success(request, "The last update was canceled.")
            return HttpResponseRedirect(self.return_url)

        if 'next' in list(request.POST.keys()) or 'finish' in list(
                request.POST.keys()):
            self.current_form_set = self.form_sets[self.step]
            if not self.current_form_set['the_form']:
                return self.return_on_error(request, "STEP_ERROR")
            self.forms = self.setup_forms(
                self.current_form_set['the_form'],
                request)
            if ("is_formset" not in self.current_form_set or (
                    not self.current_form_set['is_formset'])) and len(
                    self.forms) == 0:
                return self.return_on_error(request, "NO_FORM_ERROR")

            if not self.validate_forms():
                self.step = self.step - 1
                self.current_form_set = self.form_sets[self.step]
                context = self.make_context(request, valid=False)
                return render(request, self.template, context)
            is_finished = self.finish_valid_form(request)
            if 'finish' in list(request.POST.keys()) or (
                    is_finished is not None and is_finished):
                return HttpResponseRedirect(self.finish(request))

        else:
            msg = UserMessage.objects.get_or_create(
                view=self.__class__.__name__,
                code="BUTTON_CLICK_UNKNOWN",
                defaults={
                    'summary': user_messages["BUTTON_CLICK_UNKNOWN"]
                    ['summary'],
                    'description': user_messages["BUTTON_CLICK_UNKNOWN"]
                    ['description']}
                )
            messages.error(request, msg[0].description)
            self.current_form_set = {'next_form': None}

        if self.current_form_set['next_form'] is not None:
            self.forms = self.setup_forms(self.current_form_set['next_form'])
            context = self.make_context(request)
            return render(request, self.template, context)

        return HttpResponseRedirect(self.return_url)

import os
from pathlib import Path
from random import shuffle

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Question, QuestionsUpdate
from .questionsupdater import QuestionsUpdater


class IndexView(generic.ListView):
    template_name = 'cards/index.html'
    paginate_by = "5"

    def get_queryset(self):
        questions_all = []

        [questions_all.append(i) for i in list(Question.objects.all().order_by('question_number'))]

        get_request = self.request.GET

        if not self.request.session.session_key:
            self.request.session.create()
        self.request.session.set_expiry(864000)

        # in case DB changed when user has an active session
        if len(self.request.session.get('order', list(range(0, len(questions_all))))) != len(questions_all):
            for key in list(self.request.session.keys()):
                if not key.startswith("_"):  # skip keys set by the django system
                    del self.request.session[key]
            self.request.session.modified = True
            return questions_all

        if get_request.get('order'):
            self.request.session['mix_order'] = (False if get_request.get('order').__eq__("straight") else True)
            self.request.session['order_changed'] = True
        else:
            self.request.session['mix_order'] = self.request.session.get('mix_order', False)
            self.request.session['order_changed'] = False

        if len(get_request) > 0:
            self.request.session['refresh'] = True
            self.request.session['current_page'] = (get_request.get('page') if get_request.get('page') else 1)
        else:
            self.request.session['refresh'] = False
            self.request.session['current_page'] = self.request.session.get('current_page', 1)

        group_current = self.request.session.get('current_group', "All")
        if get_request.get('question-group'):
            self.request.session['group_changed'] = True
            self.request.session['current_group'] = get_request.get('question-group')
            self.request.session['current_page'] = 1
        else:
            self.request.session['group_changed'] = False
            self.request.session['current_group'] = group_current
            self.request.session['current_page'] = self.request.session.get('current_page', 1)

        self.request.session['num_objects'] = (get_request.get('num-objects') if get_request.get('num-objects')
                                               else self.request.session.get('num_objects', self.paginate_by))

        if self.request.session.get('order_changed', False):
            if self.request.session.get('mix_order', False):
                mix_order = list(range(0, len(questions_all)))
                shuffle(mix_order)
                self.request.session['order'] = mix_order
            else:
                self.request.session['order'] = list(range(0, len(questions_all)))
        else:
            self.request.session['order'] = self.request.session.get('order', list(range(0, len(questions_all))))

        questions_for_return_all = []
        [questions_for_return_all.append(questions_all[i]) for i in
         self.request.session.get('order', list(range(0, len(questions_all))))]

        if group_current.__eq__("All"):
            return questions_for_return_all
        else:
            questions_for_return = []
            for q in questions_for_return_all:
                if q.question_group.__eq__(group_current):
                    questions_for_return.append(q)
            return questions_for_return

    def get_context_data(self, **kwargs):

        context = super(IndexView, self).get_context_data(**kwargs)

        context['current_group'] = self.request.session.get('current_group', "All")

        groups_list = list(Question.objects.values_list('question_group', flat=True).distinct())
        groups_list.insert(0, "All")
        context['groups_list'] = groups_list

        page = self.request.session.get('current_page', 1)

        paginate_by_user = self.request.session.get('num_objects', self.paginate_by)

        context['num_objects'] = paginate_by_user

        context['num_objects_array'] = ["5", "10", "20", "All"]

        context['mix_order'] = self.request.session.get('mix_order', False)

        context['refresh'] = self.request.session.get('refresh', False)

        if paginate_by_user.__eq__("All"):
            context['latest_question_list'] = self.get_queryset()
        else:
            paginator = Paginator(self.get_queryset(), int(paginate_by_user))
            context['latest_question_list'] = paginator.get_page(page)

        return context


@staff_member_required
def update_questions_list(*args, **kwargs):
    file_path = QuestionsUpdate.objects.get(id=kwargs["question_list_id"]).file.path
    if not os.path.isfile(file_path):
        return HttpResponseRedirect(reverse('admin:cards_questionsupdate_changelist', args=(), current_app='cards'))
    replace_all_questions(file_path)
    return HttpResponseRedirect(reverse('admin:cards_questionsupdate_changelist', args=(), current_app='cards'))


def update_questions_list_prefilled(request):
    root_dir = Path(__file__).resolve().parent
    file_path = os.path.join(root_dir, 'uploads', 'CivicsQuestions2008.txt')
    if not os.path.isfile(file_path):
        messages.add_message(request, messages.INFO, 'Could not load the prefilled questions. Click to dismiss.')
        return HttpResponseRedirect(reverse('cards:index', args=(), current_app='cards'))
    replace_all_questions(file_path)
    return HttpResponseRedirect(reverse('cards:index', args=(), current_app='cards'))


def replace_all_questions(file_path):
    # wiping all the existing questions
    with transaction.atomic():
        for q_object in Question.objects.all():
            q_object.delete()

    # creating new questions and answers
    questions_new = QuestionsUpdater(file_path).questions
    questions_new.reverse()
    with transaction.atomic():
        for q in questions_new:
            question = Question(question_text=q.question_text, question_number=q.question_id,
                                pub_date=timezone.now(),
                                question_group=q.question_group, question_group_title=q.question_group_title)
            question.save()
            for count, value in enumerate(q.answer_text):
                question.answer_set.create(answer_text=value, answer_correct=q.answer_correct[count]).save()

from random import shuffle

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
    # updating the questions on server load
    questions_all = list(Question.objects.all().order_by('question_number'))
    paginate_by = "5"

    def get_queryset(self):
        questions_for_return = []
        get_request = self.request.GET

        if not self.request.session.session_key:
            self.request.session.create()
        self.request.session.set_expiry(7200)

        if get_request.get('order'):
            if get_request.get('order').__eq__("straight"):
                self.request.session['order'] = list(range(0, len(self.questions_all)))
                self.request.session['order_type'] = "straight"
            else:
                user_order = list(range(0, len(self.questions_all)))
                shuffle(user_order)
                self.request.session['order'] = user_order
                self.request.session['order_type'] = "mix"

        all_questions_for_return = []
        for i in self.request.session.get('order', list(range(0, len(self.questions_all)))):
            all_questions_for_return.append(self.questions_all[i])

        if get_request.get('question_group'):
            group_current = get_request.get('question_group')
            if group_current.__eq__("All"):
                return all_questions_for_return
            else:
                for q in all_questions_for_return:
                    if q.question_group.__eq__(group_current):
                        questions_for_return.append(q)
                return questions_for_return

        return all_questions_for_return

    def get_context_data(self, **kwargs):

        context = super(IndexView, self).get_context_data(**kwargs)

        get_request = self.request.GET

        current_group = "All"
        if get_request.get('question_group'):
            current_group = get_request.get('question_group')
        context['current_group'] = current_group

        groups_list = list(Question.objects.values_list('question_group', flat=True).distinct())
        groups_list.insert(0, "All")
        context['groups_list'] = groups_list

        page = 1
        if get_request.get('page'):
            page = get_request.get('page')

        paginate_by_user = self.request.session.get('paginate-by-user', self.paginate_by)
        if get_request.get('num-objects'):
            paginate_by_user = get_request.get('num-objects')

        self.request.session['paginate-by-user'] = paginate_by_user
        context['num_objects'] = paginate_by_user
        context['num_objects_array'] = ["5", "10", "20", "All"]

        if self.request.session.get('order_type', "straight").__eq__("mix"):
            context['mix_order'] = True
        else:
            context['mix_order'] = False

        if paginate_by_user.__eq__("All"):
            context['latest_question_list'] = self.get_queryset()
        else:
            paginator = Paginator(self.get_queryset(), int(paginate_by_user))
            context['latest_question_list'] = paginator.get_page(page)

        return context


@staff_member_required
def update_questions_list(*args, **kwargs):
    print(args)

    file_path = QuestionsUpdate.objects.get(id=kwargs["question_list_id"]).file.path

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

    return HttpResponseRedirect(reverse('admin:cards_questionsupdate_changelist', args=(), current_app='cards'))

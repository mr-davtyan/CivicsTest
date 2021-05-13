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
    questions_all: list

    def get_queryset(self):
        self.questions_all = Question.objects.all().order_by('question_number')
        # todo add mix button
        # todo save mix state
        questions_for_return = []
        request = self.request.GET
        if request.get('question_group'):
            group_current = request.get('question_group')
            if group_current.__eq__("All"):
                return self.questions_all
            else:
                for q in self.questions_all:
                    if q.question_group.__eq__(group_current):
                        questions_for_return.append(q)
                return questions_for_return
        return self.questions_all

    def get_context_data(self, **kwargs):

        context = super(IndexView, self).get_context_data(**kwargs)

        request = self.request.GET
        current_group = "All"
        if request.get('question_group'):
            current_group = request.get('question_group')
        context['current_group'] = current_group

        groups_list = list(Question.objects.values_list('question_group', flat=True).distinct())
        groups_list.insert(0, "All")
        context['groups_list'] = groups_list

        # todo add pagintaor value on the web site
        paginate_by = 2
        paginator = Paginator(self.get_queryset(), paginate_by)

        page = 1
        if request.get('page'):
            page = request.get('page')

        context['latest_question_list'] = paginator.get_page(page)

        return context


@staff_member_required
def update_questions_list(request, question_list_id):
    file_path = QuestionsUpdate.objects.get(id=question_list_id).file.path

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

from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Question, QuestionsUpdate
from .questionsupdater import QuestionsUpdater


class IndexView(generic.ListView):
    template_name = 'cards/index.html'

    def get_queryset(self):
        if self.request.GET.get('question_group'):
            featured_filter = self.request.GET.get('question_group')
            if featured_filter.__eq__("All"):
                return Question.objects.all().order_by('?')
            else:
                return Question.objects.filter(question_group__contains=featured_filter).order_by('?')
        else:
            """
            Return  in random order. Please note that this approach can be very slow, as documented.
            """
            return Question.objects.all().order_by('?')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        t_list = list(Question.objects.values_list('question_group', flat=True).distinct())
        t_list.insert(0, "All")
        context['groups_list'] = t_list
        context['latest_question_list'] = self.get_queryset()
        return context


class DetailView(generic.DetailView):
    model = Question
    template_name = 'cards/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


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

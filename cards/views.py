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
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        # return Question.objects.filter(
        #     pub_date__lte=timezone.now()
        # ).order_by('-pub_date')[:5]
        # """
        # Return everything
        # """
        # return Question.objects.all()

        """
        Return  in random order. Please note that this approach can be very slow, as documented.
        """
        return Question.objects.order_by('?')

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

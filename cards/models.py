import datetime

from django.contrib import admin
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=2000, default='')
    question_text.verbose_name = 'question'
    question_number = models.IntegerField(default=0)
    question_number.verbose_name = '#'
    pub_date = models.DateTimeField('date published')
    question_group = models.CharField(max_length=600, default='')
    question_group.verbose_name = 'group'
    question_group_title = models.CharField(max_length=600, default='')
    question_group_title.verbose_name = 'series'

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=2000, default='')
    answer_correct = models.BooleanField(True)
    answer_correct.verbose_name = 'Correct Answer'

    def __str__(self):
        return self.answer_text

    def is_correct(self):
        return self.answer_correct.get_prep_value


class QuestionsUpdate(models.Model):
    file = models.FileField(upload_to='cards/uploads')

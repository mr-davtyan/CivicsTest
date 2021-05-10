from django.contrib import admin

from .models import Question, Answer, QuestionsUpdate


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3
    list_display = ('question_text', 'question_number', 'question_group', 'question_group_title', 'pub_date', 'was_published_recently')


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        (None, {'fields': ['question_number']}),
        (None, {'fields': ['question_group']}),
        (None, {'fields': ['question_group_title']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [AnswerInline]
    list_display = ('question_text', 'question_number', 'question_group', 'question_group_title', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionsUpdate)

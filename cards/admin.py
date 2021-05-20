from django.contrib import admin

from .models import Question, Answer, QuestionsUpdate


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3
    list_display = ('question_text', 'question_number', 'question_group', 'question_group_title', 'pub_date')


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        (None, {'fields': ['question_number']}),
        (None, {'fields': ['question_group']}),
        (None, {'fields': ['question_group_title']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [AnswerInline]
    list_display = ('question_text', 'question_number', 'question_group', 'question_group_title', 'pub_date')
    list_filter = ['question_group', 'question_group_title']
    search_fields = ['question_text']


class QuestionsUpdateAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['file_name']}),
        (None, {'fields': ['file']}),
        (None, {'fields': ['file_description']}),
    ]
    list_display = ('file_name', 'file', 'file_description')
    list_filter = ['file_name']
    search_fields = ['file_name', 'file_description']


admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionsUpdate, QuestionsUpdateAdmin)

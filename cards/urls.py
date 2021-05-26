from django.urls import path, include

from . import views

app_name = 'cards'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path(
        '<int:question_list_id>/update-questions-list',
        views.update_questions_list,
        name='update-questions-list'
    ),
    path(
        'prefilled-update',
        views.update_questions_list_prefilled,
        name='update-questions-list-prefilled'
    ),

]
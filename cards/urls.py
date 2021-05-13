from django.urls import path, include

from . import views

app_name = 'cards'
urlpatterns = [
    # (r'^admin/', include(admin.site.urls) ),
    path('', views.IndexView.as_view(), name='index'),
    path(
        '<int:question_list_id>/update-questions-list',
        views.update_questions_list,
        name='update-questions-list'
    ),


]
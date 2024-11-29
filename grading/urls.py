from django.urls import path
from . import views

urlpatterns = [
    path('grading', views.home, name='home'),
    path('create_question/', views.create_question, name='create_question'),
    path('select_test/', views.select_test, name='select_test'),
    path('start_test/<int:test_id>/', views.start_test, name='start_test'),
    path('answer_question/<int:question_id>/', views.answer_question, name='answer_question'),
    path('submit_answers/<int:test_id>/', views.submit_answers, name='submit_answers'),
    path('show_results/<int:test_id>/', views.show_results, name='show_results'),
    path('set_grading_criteria/', views.set_grading_criteria, name='set_grading_criteria'),
]

# StudentList/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('student_list/', views.student_list, name='student_list'),
    path('student/edit/<int:student_id>/', views.edit_student, name='edit_student'),
]

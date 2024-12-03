# StudentList/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('student_list/', views.student_list, name='student_list'),
    path('student/edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('delete_student/<str:student_id>/', views.delete_student, name='delete_student'),  # 削除用のURL
]

# StudentList/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('teacher_list/', views.teacher_list, name='teacher_list'),
    path('teacher/edit/<int:teacher_id>/', views.edit_teacher, name='edit_teacher'),
    path('delete_teacher/<str:teacher_id>/', views.delete_teacher, name='delete_teacher'),  # 削除用のURL
]

from django.urls import path
from . import views

urlpatterns = [
    path('student_login/', views.student_login_view, name='student_login'),
    path('teacher_login/', views.teacher_login_view, name='teacher_login'),
    path('studentmenu/', views.student_menu_view, name='studentmenu'),
    path('teachermenu/', views.teacher_menu_view, name='teachermenu'),
    path('logout/', views.logout_view, name='logout'),
]

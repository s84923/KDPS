from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Django 管理画面
    path('', include('KDPS.urls')),  # KDPS アプリの URL
    path('accounts/', include('accounts.urls')),  # accounts アプリの URL
    path('accounts/', include('django.contrib.auth.urls')),  # Django 認証URL
    path('exam/', include('Exam.urls')),  # Exam アプリの URL
    path('studentmenu/', include('studentmenu.urls')),  # studentmenu アプリの URL
    path('grades/', include('Grades.urls')),  # Grades アプリの URL
    path('grademenu/', include('Grademenu.urls')),  # Grademenu アプリの URL
    path('login/', include('login.urls')),  # login アプリの URL
    path('verification/', include('two_step_verification.urls')),  # two_step_verification アプリの URL
    path('student_register/', include('student_register.urls')),  # student_register アプリの URL
    path('teacher_register/', include('teacher_register.urls')),  # teacher_register アプリの URL
    path('permissions/', include('permissions.urls')),  # permissions アプリの URL
    path('students/', include('StudentList.urls')),  # StudentList アプリの URL
    path('dbzikken/', include('DBzikken.urls')),  # DBzikken アプリの URL
    path('test_list/', include('test_list.urls')),  # test_list アプリの URL
    path('log_action/', include('Log_Action.urls')),  # Log_Action アプリの URL
    path('log_error/', include('Log_Error.urls')),  # Log_Error アプリの URL
    path('grading/', include('grading.urls')),  # grading アプリの URL
    path('teachers/', include('TeacherList.urls')),  # TeacherList アプリの URL
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),         # Django 管理画面
    path('', include('KDPS.urls')),          # KDPS アプリの URL をインクルード
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Django 認証URLをインクルード
    path('', include('Exam.urls')),  # Exam のURLをインクルード
    path('', include('studentmenu.urls')),
    path('', include('Grades.urls')), #Grades
    path('', include('Grademenu.urls')), 
    path('', include('login.urls')), 
    path('', include('two_step_verification.urls')), 
    path('', include('student_register.urls')),
    path('', include('teacher_register.urls')),
    path('', include('new_tests.urls')),
    path('', include('permissions.urls')),

]
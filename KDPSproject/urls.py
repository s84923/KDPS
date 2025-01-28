from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Django 管理画面
    path('', lambda request: redirect('student_login'), name='root'),  # ルートをログインページへリダイレクト
    path('', include('KDPS.urls')),
    path('teachermenu/', include('KDPS.urls')), 
    # 各アプリのURLパターンを整理
    path('accounts/', include('accounts.urls')),
    path('auth/', include('django.contrib.auth.urls')),  # Django 標準認証用URL
    path('exam/', include('Exam.urls')),  # Exam アプリ
    path('studentmenu/', include('studentmenu.urls')),  # 学生メニュー
    path('grades/', include('Grades.urls')),  # 成績関連
    path('grademenu/', include('Grademenu.urls')),  # 成績メニュー
    path('login/', include('login.urls')),  # ログイン関連
    path('verification/', include('two_step_verification.urls')),  # 二段階認証
    path('student_register/', include('student_register.urls')),  # 生徒登録
    path('teacher_register/', include('teacher_register.urls')),  # 教員登録
    path('permissions/', include('permissions.urls')),  # 権限管理
    path('students/', include('StudentList.urls')),  # 生徒リスト
    path('dbzikken/', include('DBzikken.urls')),  # DB実験
    path('test_list/', include('test_list.urls')),  # テスト一覧
    path('log_action/', include('Log_Action.urls')),  # アクションログ
    path('log_error/', include('Log_Error.urls')),  # エラーログ
    path('grading/', include('grading.urls')),  # 採点
    path('teachers/', include('TeacherList.urls')),  # 教員リスト
    path('studentgrades/', include('StudentGrades.urls')),  # StudentGradesをインクルード

]

# 開発環境での静的ファイルの提供
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

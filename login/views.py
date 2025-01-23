from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentLoginForm, TeacherLoginForm
from KDPS.models import Student, Teacher

# 生徒ログインビュー
def student_login_view(request):
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data.get('student_id')
            password = form.cleaned_data.get('password')

            try:
                student = Student.objects.get(student_id=student_id)
                if student.password == password:  # 単純比較に変更（非常に危険）
                    # ログイン成功
                    request.session['user_type'] = 'student'
                    request.session['user_id'] = student.student_id
                    messages.success(request, "ログイン成功")
                    return redirect('studentmenu')  # 生徒用メニューへリダイレクト
                else:
                    messages.error(request, "パスワードが正しくありません")
            except Student.DoesNotExist:
                messages.error(request, "学籍番号が存在しません")
        else:
            messages.error(request, "フォームの入力が正しくありません")
    else:
        form = StudentLoginForm()

    return render(request, 'login/student_login.html', {'form': form})

# 教員ログインビュー
def teacher_login_view(request):
    if request.method == 'POST':
        form = TeacherLoginForm(request.POST)
        if form.is_valid():
            teacher_id = form.cleaned_data.get('teacher_id')
            password = form.cleaned_data.get('password')

            try:
                teacher = Teacher.objects.get(teacher_id=teacher_id)
                if teacher.password == password:  # 単純比較に変更（非常に危険）
                    # ログイン成功
                    request.session['user_type'] = 'teacher'
                    request.session['user_id'] = teacher.teacher_id
                    messages.success(request, "ログイン成功")
                    return redirect('teachermenu')  # 教員用メニューへリダイレクト
                else:
                    messages.error(request, "パスワードが正しくありません")
            except Teacher.DoesNotExist:
                messages.error(request, "教員IDが存在しません")
        else:
            messages.error(request, "フォームの入力が正しくありません")
    else:
        form = TeacherLoginForm()

    return render(request, 'login/teacher_login.html', {'form': form})

# 生徒用メニュー
def student_menu_view(request):
    if request.session.get('user_type') == 'student':
        return render(request, 'studentmenu/studentmenu.html')  # 生徒用メニューの表示
    messages.error(request, "不正なアクセスです")
    return redirect('student_login')  # 不正アクセスの場合、ログインページにリダイレクト

# 教員用メニュー
def teacher_menu_view(request):
    if request.session.get('user_type') == 'teacher':
        return render(request, 'KDPS/index.html')  # 教員用メニューの表示
    messages.error(request, "不正なアクセスです")
    return redirect('teacher_login')  # 不正アクセスの場合、ログインページにリダイレクト

# ログアウトビュー
def logout_view(request):
    request.session.flush()  # セッションのクリア
    messages.success(request, "ログアウトしました")
    return redirect('student_login')  # ログインページにリダイレクト

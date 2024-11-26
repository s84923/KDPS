from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            password = form.cleaned_data['password']
            user = authenticate(request, username=student_id, password=password)
            if user is not None:
                login(request, user)
                
                # ユーザーのロールに応じたリダイレクト先
                if user.profile.role == 'student':
                    return redirect('student_dashboard')  # 学生用ダッシュボード
                elif user.profile.role == 'teacher':
                    return redirect('teacher_dashboard')  # 教師用ダッシュボード
                elif user.profile.role == 'admin':
                    return redirect('admin_dashboard')  # 管理者用ダッシュボード
                else:
                    return HttpResponse("ユーザーの役職が設定されていません。")
            else:
                form.add_error(None, "学籍番号またはパスワードが間違っています。")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def login_redirect(request):
    # ユーザーが生徒の場合は生徒ダッシュボードへ
    if request.user.profile.role == 'student':
        return redirect('student_dashboard')
    # ユーザーが教師の場合は教師用ダッシュボードへ
    elif request.user.profile.role == 'teacher':
        return redirect('teacher_dashboard')
    else:
        # デフォルトのリダイレクト先（管理者用）
        return redirect('admin_dashboard')

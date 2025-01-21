from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as AuthUser
from django.contrib import messages
from .forms import LoginForm

# ログインビュー
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data.get('student_ID')
            password = form.cleaned_data.get('password')

            # Djangoの標準認証システムを使用
            user = authenticate(request, username=student_id, password=password)
            if user is not None:
                login(request, user)
                # ログイン後のリダイレクト先をユーザーの役職で変更
                if hasattr(user, 'profile'):
                    if user.profile.role == 'student':
                        return redirect('student_dashboard')  # 生徒用画面
                    elif user.profile.role == 'teacher':
                        return redirect('teacher_dashboard')  # 教員用画面
                    else:
                        messages.error(request, "ユーザーの役職が設定されていません。")
                else:
                    messages.error(request, "ユーザーのプロフィールが設定されていません。")
            else:
                messages.error(request, "学籍番号またはパスワードが間違っています。")
        else:
            messages.error(request, "入力データが正しくありません。")
        return render(request, 'login.html', {'form': form})

    # GETリクエスト時の処理
    form = LoginForm()
    return render(request, 'login.html', {'form': form})

# ログイン後にリダイレクトするビュー（例）
@login_required
def student_dashboard(request):
    return render(request, 'studentmenu/studentmenu.html')

@login_required
def teacher_dashboard(request):
    return render(request, 'KDPS/index.html')

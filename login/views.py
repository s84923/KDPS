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

            try:
                # 学籍番号でユーザーを検索
                user = AuthUser.objects.get(username=student_id)

                if user.check_password(password):  # パスワード認証
                    login(request, user)

                    if hasattr(user, 'profile'):
                        if user.profile.role == 'student':
                            return render(request, 'studentmenu/studentmenu.html')  # 生徒用画面
                        elif user.profile.role == 'teacher':
                            return render(request, 'KDPS/index.html')  # 教員用画面
                        elif user.profile.role == 'admin':
                            return redirect('admin_dashboard')  # 管理者用
                        else:
                            messages.error(request, "ユーザーの役職が設定されていません。")
                    else:
                        messages.error(request, "ユーザーのプロフィールが設定されていません。")
                else:
                    messages.error(request, "学籍番号またはパスワードが間違っています。")
            except AuthUser.DoesNotExist:
                messages.error(request, "学籍番号またはパスワードが間違っています。")
        else:
            messages.error(request, "入力データが正しくありません。")
        
        return render(request, 'login.html', {'form': form})
    
    form = LoginForm()
    return render(request, 'login.html', {'form': form})

# ログイン後にリダイレクトするビュー
@login_required
def login_redirect(request):
    if hasattr(request.user, 'profile'):
        if request.user.profile.role == 'student':
            return render(request, 'studentmenu/studentmenu.html')  # 生徒用画面
        elif request.user.profile.role == 'teacher':
            return render(request, 'KDPS/index.html')  # 教員用画面
        else:
            return redirect('admin_dashboard')  # 管理者用
    else:
        return HttpResponse("ユーザーのプロフィールが設定されていません。")

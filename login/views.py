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
                    return render(request, 'studentmenu/studentmenu.html')  # 生徒用画面
                elif user.profile.role == 'teacher':
                    return render(request, 'KDPS/index.html')  # 教員用画面
                elif user.profile.role == 'admin':
                    return redirect('admin_dashboard')  # 管理者用（必要なURLに変更）
                else:
                    return HttpResponse("ユーザーの役職が設定されていません。")
            else:
                form.add_error(None, "学籍番号またはパスワードが間違っています。")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def login_redirect(request):
    # ユーザーが生徒の場合は生徒用画面にリダイレクト
    if request.user.profile.role == 'student':
        return render(request, 'studentmenu/studentmenu.html')  # 生徒用画面

    # ユーザーが教師の場合は教師用画面にリダイレクト
    elif request.user.profile.role == 'teacher':
        return render(request, 'KDPS/index.html')  # 教員用画面

    # その他の場合（管理者用など）
    else:
        return redirect('admin_dashboard')  # 管理者用（必要なURLに変更）

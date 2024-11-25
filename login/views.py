from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.http import HttpResponse

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
                if user.role == 'student':
                    return redirect('student_home')  # 学生用のホーム
                elif user.role == 'teacher':
                    return redirect('teacher_home')  # 教師用のホーム
                elif user.role == 'admin':
                    return redirect('admin_home')  # 管理者用のホーム
                else:
                    return HttpResponse("ユーザーの役職が設定されていません。")
            else:
                form.add_error(None, "学籍番号またはパスワードが間違っています。")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

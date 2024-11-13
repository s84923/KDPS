from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserForm  # UserFormがユーザー登録用のフォームとしてある前提

def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_users')  # データ保存後に一覧ページにリダイレクト
    else:
        form = UserForm()
    return render(request, 'DBzikken/add_user.html', {'form': form})

def user_list(request):
    users = User.objects.all()
    return render(request, 'DBzikken/user_list.html', {'users': users})

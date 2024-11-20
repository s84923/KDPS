# views.py
from django.shortcuts import render
from .forms import LoginForm
from django import forms

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # ログイン処理
            student_ID = form.cleaned_data['student_ID']
            password = form.cleaned_data['password']
            # ここに認証処理を追加
            print(f"学籍番号: {student_ID}, パスワード: {password}")
            # 成功時のリダイレクトを追加
        else:
            print("無効なフォームです")
    else:
        form = LoginForm()

    return render(request, 'login/login.html', {'form': form})


class LoginForm(forms.Form):
    student_ID = forms.CharField(
        label="学籍番号(ID)",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '学籍番号(ID)を入力してください',
        })
    )
    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'パスワードを入力してください',
            'id': 'input_pass'  # JavaScriptで参照するためのID
        })
    )


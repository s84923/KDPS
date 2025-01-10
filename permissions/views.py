# views.py
from django.shortcuts import render, get_object_or_404, redirect
from KDPS.models import User
from django import forms
from django.http import HttpResponse
from django.contrib import messages

# フォーム定義
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['student_name', 'school_year', 'student_class', 'parent_email', 'address']
        widgets = {
            'student_name': forms.TextInput(attrs={'placeholder': '名前'}),
            'school_year': forms.NumberInput(attrs={'placeholder': '学年'}),
            'student_class': forms.TextInput(attrs={'placeholder': 'クラス'}),
            'parent_email': forms.EmailInput(attrs={'placeholder': '保護者メールアドレス'}),
            'address': forms.TextInput(attrs={'placeholder': '住所'}),
        }

def permission_edit(request):
    # 編集するデータをテンプレートに渡したい場合は、contextに追加します
    context = {
        # 例: "users": users
    }
    return render(request, 'permissions/permissions.html', context)

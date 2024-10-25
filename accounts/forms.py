# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="メールアドレス")
    student_id = forms.CharField(max_length=20, required=True, label="学籍番号(ID)", error_messages={'required': '学籍番号を入力してください'})
    grade = forms.IntegerField(min_value=1, max_value=6, required=True, label="学年", error_messages={'required': '学年を入力してください'})
    class_name = forms.CharField(max_length=50, required=True, label="クラス", error_messages={'required': 'クラスを入力してください'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'student_id', 'grade', 'class_name']
        labels = {
            'username': '氏名',  # ユーザー名を「氏名」に変更
        }


    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                student_id=self.cleaned_data['student_id'],
                grade=self.cleaned_data['grade'],
                class_name=self.cleaned_data['class_name'],
            )
        return user

from django import forms
from django.shortcuts import render, redirect
from KDPS.models import Student, User

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_id', 'student_id', 'password', 'authority', 'role']
        labels = {
            'user_id': 'ユーザーID',
            'student_id': '生徒ID',
            'password': 'パスワード',
            'authority': '権限',
            'role': '役職',
        }
        widgets = {
            'user_id': forms.TextInput(attrs={'placeholder': 'ユーザーIDを入力', 'style': 'width: 100%;'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'パスワードを入力', 'style': 'width: 100%;'}),
            'authority': forms.Select(attrs={'style': 'width: 100%;'}),
            'role': forms.Select(attrs={'style': 'width: 100%;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # authority フィールドに対して choices をセット
        self.fields['authority'].choices = [
            (1, '学生'),
            (2, '教師'),
            (3, '管理者'),
        ]

        # authority の値に基づいて role を制御
        authority = self.initial.get('authority', 1)  # デフォルトで学生に設定

        # authority に基づいて role を制御
        if authority == 1:
            self.fields['role'].initial = 'student'
            self.fields['role'].choices = [('student', '学生')]
        elif authority == 2:
            self.fields['role'].initial = 'teacher'
            self.fields['role'].choices = [('teacher', '教師')]
        elif authority == 3:
            self.fields['role'].initial = 'admin'
            self.fields['role'].choices = [('admin', '管理者')]

        # authority フィールドにデフォルト値をセットする
        if not self.fields['authority'].initial:
            self.fields['authority'].initial = 1  # デフォルトで学生に設定


class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'student_name', 'school_year', 'student_class', 'email', 'parent_email', 'address']
        labels = {
            'student_id': '学籍番号',
            'student_name': '生徒氏名',
            'school_year': '学年',
            'student_class': 'クラス',
            'email': 'メールアドレス',
            'parent_email': '保護者メールアドレス',
            'address': '住所',
        }
        widgets = {
            'student_id': forms.TextInput(attrs={'placeholder': '学籍番号を入力', 'style': 'width: 100%;'}),
            'student_name': forms.TextInput(attrs={'placeholder': '生徒名を入力', 'style': 'width: 100%;'}),
            'school_year': forms.NumberInput(attrs={'placeholder': '学年を入力', 'style': 'width: 100%;'}),
            'student_class': forms.TextInput(attrs={'placeholder': 'クラスを入力', 'style': 'width: 100%;'}),
            'email': forms.EmailInput(attrs={'placeholder': 'メールアドレスを入力', 'style': 'width: 100%;'}),
            'parent_email': forms.EmailInput(attrs={'placeholder': '保護者メールアドレスを入力', 'style': 'width: 100%;'}),
            'address': forms.TextInput(attrs={'placeholder': '住所を入力', 'style': 'width: 100%;'}),
        }

def student_register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        user_form = UserRegistrationForm(request.POST)

        if form.is_valid() and user_form.is_valid():
            # 新しい生徒情報を保存
            student = form.save()

            # 新しいユーザー情報を保存（user_idを自動で割り当て）
            user = user_form.save(commit=False)
            user.student_id = student  # 生徒情報をユーザーに紐づけ
            user.user_id = User.objects.latest('user_id').user_id + 1 if User.objects.exists() else 1  # user_idを自動割り当て
            user.save()

            return redirect('student_register')  # 登録成功後のページへリダイレクト
    else:
        form = StudentRegistrationForm()
        user_form = UserRegistrationForm()

    return render(request, 'student_register/student_register.html', {'form': form, 'user_form': user_form})
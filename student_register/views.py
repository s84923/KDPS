from django import forms
from django.shortcuts import render, redirect
from KDPS.models import Student

# フォームをviews.pyに直接記述
class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id','student_name', 'school_year', 'student_class', 'email', 'parent_email', 'address']
        labels = {
            'student_id' : '学籍番号',
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
        if form.is_valid():
            form.save()  # 新規生徒情報を保存
            return redirect('student_register')  # 登録成功後のページへリダイレクト
    else:
        form = StudentRegistrationForm()

    return render(request, 'student_register/student_register.html', {'form': form})

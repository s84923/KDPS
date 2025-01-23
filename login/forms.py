from django import forms

class StudentLoginForm(forms.Form):
    student_id = forms.IntegerField(
        label="学籍番号",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '学籍番号を入力してください'})
    )
    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'パスワードを入力してください'})
    )

class TeacherLoginForm(forms.Form):
    teacher_id = forms.CharField(
        label="教員ID",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '教員IDを入力してください'})
    )
    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'パスワードを入力してください'})
    )

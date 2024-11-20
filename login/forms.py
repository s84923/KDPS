from django import forms

class LoginForm(forms.Form):
    student_ID = forms.CharField(
        label="学籍番号(ID)",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '学籍番号(ID)を入力して下さい',
            'required': 'required'
        })
    )
    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'パスワードを入力して下さい',
            'required': 'required'
        })
    )

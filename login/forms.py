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

    def clean(self):
        cleaned_data = super().clean()
        student_ID = cleaned_data.get("student_ID")
        password = cleaned_data.get("password")

        if not student_ID or not password:
            raise forms.ValidationError("学籍番号(ID)とパスワードを両方入力してください。")


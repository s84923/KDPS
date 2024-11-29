# forms.py
from django import forms
from KDPS.models import Teacher, User

class TeacherForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'パスワード'}))

    class Meta:
        model = Teacher
        fields = ['teacher_name', 'school_year', 'email', 'student_class', 'post', 'teacher_id', 'password']

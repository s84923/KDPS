# forms.py
from django import forms
from KDPS.models import Student

class StudentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'パスワード'}))

    class Meta:
        model = Student
        fields = ['student_id', 'student_name', 'school_year', 'student_class', 'email', 'parent_email', 'address', 'password']
       
from django import forms
from KDPS.models import Teacher

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['teacher_id', 'teacher_name', 'school_year', 'student_class', 'post']
        widgets = {
            'teacher_id': forms.TextInput(attrs={'placeholder': '教員ID'}),
            'teacher_name': forms.TextInput(attrs={'placeholder': '教員氏名'}),
            'school_year': forms.NumberInput(attrs={'placeholder': '担当学年'}),
            'student_class': forms.TextInput(attrs={'placeholder': '担当クラス'}),
            'post': forms.TextInput(attrs={'placeholder': '役職'}),
        }

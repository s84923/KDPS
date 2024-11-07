# forms.py
from django import forms

class ExamCreationForm(forms.Form):
    grade_select = forms.ChoiceField(
        choices=[('', '選択してください'), ('1', '1年'), ('2', '2年'), ('3', '3年')],
        label='学年'
    )
    class_grade = forms.ChoiceField(
        choices=[('', '選択してください'), ('A', 'A組'), ('B', 'B組'), ('C', 'C組')],
        label='クラス'
    )
    teacher_mail = forms.EmailField(
        label='試験名',
        widget=forms.TextInput(attrs={'placeholder': '試験名を入力してください'})
    )
    class_name = forms.CharField(
        label='教員ID',
        widget=forms.TextInput(attrs={'placeholder': '教員IDを入力してください'})
    )

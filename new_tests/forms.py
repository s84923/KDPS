# forms.py
from django import forms

class ExamCreationForm(forms.Form):
    test_id = forms.CharField(
        label='クラス',
        widget=forms.TextInput(attrs={'placeholder': '試験IDを入力して下さい'})
    )
    test_name = forms.CharField(
        label='試験名',
        widget=forms.TextInput(attrs={'placeholder': '試験名を入力してください'})
    )
    teacher_id = forms.CharField(
        label='教員ID',
        widget=forms.TextInput(attrs={'placeholder': '教員IDを入力してください'})
    )

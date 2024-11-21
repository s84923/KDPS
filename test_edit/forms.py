from django import forms

class ExamEditForm(forms.Form):
    exam_id = forms.CharField(
        label='試験ID',
        widget=forms.TextInput(attrs={'placeholder': '試験IDを入力', 'style': 'width: 100%;'})
    )
    exam_name = forms.CharField(
        label='試験名', 
        widget=forms.TextInput(attrs={'placeholder': '試験名を入力', 'style': 'width: 100%;'})
    )
    teacher_id = forms.CharField(
        label='教員ID',
        widget=forms.TextInput(attrs={'placeholder': '教員IDを入力', 'style': 'width: 100%;'})
    )

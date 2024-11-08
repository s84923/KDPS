from django import forms

class ExamEditForm(forms.Form):
    exam_name = forms.CharField(
        label='試験名', 
        widget=forms.TextInput(attrs={'placeholder': '試験名を入力', 'style': 'width: 100%;'})
    )
    target_grade = forms.ChoiceField(
        label='対象学年',
        choices=[('', '選択してください'), ('1年', '1年'), ('2年', '2年'), ('3年', '3年')],
        widget=forms.Select(attrs={'style': 'width: 100%;'})
    )
    target_class = forms.ChoiceField(
        label='対象クラス',
        choices=[('', '選択してください'), ('A組', 'A組'), ('B組', 'B組'), ('C組', 'C組')],
        widget=forms.Select(attrs={'style': 'width: 100%;'})
    )
    created_by = forms.CharField(
        label='作成教員',
        widget=forms.TextInput(attrs={'placeholder': '教員名を入力', 'style': 'width: 100%;'})
    )

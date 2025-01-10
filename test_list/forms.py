from django import forms
from KDPS.models import Test

class ExamEditForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['test_name', 'teacher_id']  # 編集可能なフィールドのみ指定
        labels = {
            'test_name': '試験名',
            'teacher_id': '教員ID',
        }
        widgets = {
            'test_name': forms.TextInput(attrs={'placeholder': '試験名を入力', 'style': 'width: 100%;'}),
            'teacher_id': forms.TextInput(attrs={'placeholder': '教員IDを入力', 'style': 'width: 100%;'}),
        }

    # 試験IDを非編集可能なフィールドとして定義
    test_id = forms.IntegerField(
        label='試験ID',
        required=False,
        widget=forms.NumberInput(attrs={
            'readonly': True,  # 読み取り専用
            'style': 'width: 100%; background-color: #e9ecef;',  # スタイル適用
        })
    )

class ExamCreationForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['test_name', 'teacher_id']  # test_idはフォームに含めない
        labels = {
            'test_name': '試験名',
            'teacher_id': '教員ID',
        }
        widgets = {
            'test_name': forms.TextInput(attrs={'placeholder': '試験名を入力', 'style': 'width: 100%;'}),
            'teacher_id': forms.TextInput(attrs={'placeholder': '教員IDを入力', 'style': 'width: 100%;'}),
        }

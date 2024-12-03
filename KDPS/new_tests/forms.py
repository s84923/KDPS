from django import forms
from KDPS.models import Test

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

from django import forms

class StudentSearchForm(forms.Form):
    student_name = forms.CharField(label="生徒名", max_length=100, required=False)
    export_format = forms.ChoiceField(
        label="エクスポート形式",
        choices=[('csv', 'CSV'), ('pdf', 'PDF')],
        required=False
    )

from django import forms
from .models import Question, Test

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['test', 'content', 'question_type', 'correct_answer', 'choices', 'score', 'partial_scoring_conditions']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'cols': 50}),
            'correct_answer': forms.Textarea(attrs={'rows': 2, 'cols': 50}),
            'choices': forms.Textarea(attrs={'rows': 3, 'cols': 50, 'placeholder': '選択肢をカンマ区切りで入力（選択問題のみ）'}),
            'partial_scoring_conditions': forms.Textarea(attrs={
                'rows': 3,
                'cols': 50,
                'placeholder': '部分点条件をカンマ区切りで入力（例: 重要なキーワード1:3, 重要なキーワード2:5）'
            }),
        }
        labels = {
            'test': '試験名',
            'content': '問題文',
            'question_type': '問題の種類',
            'correct_answer': '模範解答',
            'choices': '選択肢（選択問題のみ）',
            'score': '配点',
            'partial_scoring_conditions': '部分点条件（記述問題のみ）'
        }

    def clean_partial_scoring_conditions(self):
        """
        部分点条件のフォーマットを検証。
        正しい形式（例: "キーワード1:3, キーワード2:5"）でない場合にエラーを発生させる。
        """
        partial_scoring_conditions = self.cleaned_data.get('partial_scoring_conditions', '')
        if partial_scoring_conditions:
            conditions = partial_scoring_conditions.split(',')
            for condition in conditions:
                if ':' not in condition:
                    raise forms.ValidationError(
                        "部分点条件は 'キーワード:点数' の形式で入力してください。複数入力する場合はカンマで区切ってください。"
                    )
                key, value = condition.split(':', 1)
                if not key.strip():
                    raise forms.ValidationError("部分点条件のキーワードが空欄です。")
                if not value.strip().isdigit():
                    raise forms.ValidationError("部分点条件の点数は数値で入力してください。")
        return partial_scoring_conditions


class AnswerForm(forms.Form):
    answer = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'cols': 50,
            'placeholder': 'ここに解答を入力してください'
        }),
        label="解答"
    )

from django.db import models

class GeminiTest(models.Model):
    name = models.CharField(max_length=255)  # 試験名
    total_score = models.IntegerField(default=100)  # 試験の満点

    def __str__(self):
        return self.name


class Question(models.Model):
    QUESTION_TYPES = (
        ('objective', '選択問題'),
        ('descriptive', '記述問題'),
    )
    test = models.ForeignKey(GeminiTest, on_delete=models.CASCADE, related_name='questions', default=1)  # 試験との紐付け
    content = models.TextField()  # 問題文
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='descriptive')
    correct_answer = models.TextField()  # 正解（記述問題の場合）
    choices = models.TextField(blank=True, null=True)  # 選択肢（選択問題の場合、カンマ区切り）
    score = models.IntegerField(default=10)  # 問題ごとの配点
    partial_scoring_conditions = models.TextField(
        blank=True, null=True,
        help_text="部分点条件（記述問題用）。例: '重要なキーワード1:3, 重要なキーワード2:5'"
    )

    def get_choices(self):
        """選択肢をリスト形式で返す。空白をトリムし、重複を排除。"""
        if self.choices:
            return list(set(choice.strip() for choice in self.choices.split(',')))
        return []

    def get_partial_conditions(self):
        """
        部分点条件を辞書形式で返す。
        例: 'キーワード1:3, キーワード2:5' -> {'キーワード1': 3, 'キーワード2': 5}
        """
        if not self.partial_scoring_conditions:
            return {}
        conditions = {}
        for condition in self.partial_scoring_conditions.split(','):
            try:
                key, value = condition.split(':')
                conditions[key.strip()] = int(value.strip())
            except ValueError:
                continue
        return conditions

    def __str__(self):
        return self.content[:50]


class GradingCriteria(models.Model):
    description = models.TextField()  # 採点基準

    def __str__(self):
        return "採点基準"


class ConversationHistory(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='history', null=True, blank=True)
    user_answer = models.TextField()
    feedback = models.TextField()
    score = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question.content[:30]} - {self.timestamp}"


class TempAnswer(models.Model):
    user_id = models.IntegerField(null=True, blank=True)  # NULLを許容する
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()  # 一時保存の解答
    is_finalized = models.BooleanField(default=False)  # 最終提出済みか

    def save(self, *args, **kwargs):
        """選択問題の場合、answer_textの内容が選択肢内にあるか検証。"""
        if self.question.question_type == 'objective':
            if self.answer_text not in self.question.get_choices():
                raise ValueError(f"Invalid choice: {self.answer_text}. Must be one of {self.question.get_choices()}.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Temp Answer for {self.question.content[:30]} by User {self.user_id}"

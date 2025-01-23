from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password

# 生徒情報
class Student(models.Model):
    student_id = models.IntegerField(primary_key=True)  # 学籍番号
    student_name = models.CharField(max_length=20)  # 生徒名
    school_year = models.IntegerField()  # 学年
    student_class = models.CharField(max_length=3)  # クラス
    email = models.CharField(max_length=30)  # メールアドレス
    parent_email = models.CharField(max_length=30)  # 保護者メールアドレス
    address = models.CharField(max_length=30)  # 住所
    password = models.CharField(max_length=128)  # パスワード（ハッシュ化）

    def set_password(self, raw_password):
        """生徒のパスワードをハッシュ化して保存"""
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        """パスワードを検証"""
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.student_name

    
# 成績情報
class Grades(models.Model):
    test_id = models.ForeignKey('Test', on_delete=models.CASCADE)  # Test を文字列で指定
    student_id = models.ForeignKey('Student', on_delete=models.CASCADE)
    score = models.IntegerField()
    answer_image = models.BinaryField()

# ユーザー情報
class User(models.Model):
    ROLE_CHOICES = [
        ('student', '学生'),
        ('teacher', '教師'),
        ('admin', '管理者'),
    ]
    
    user_id = models.IntegerField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    teacher_id = models.CharField(max_length=10, null=True, blank=True)
    password = models.CharField(max_length=12)
    authority = models.IntegerField()
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')  # 役職を追加

    def __str__(self):
        return f"{self.user_id} - {self.role}"

# 教員情報
# 教員情報
class Teacher(models.Model):
    teacher_id = models.CharField(max_length=10, primary_key=True)  # 教員ID
    teacher_name = models.CharField(max_length=20)  # 教員名
    school_year = models.IntegerField()  # 学年
    email = models.CharField(max_length=30, default='')  # メールアドレス
    student_class = models.CharField(max_length=3)  # 担当クラス
    post = models.CharField(max_length=10)  # 役職
    password = models.CharField(max_length=128)  # パスワード（ハッシュ化）

    def set_password(self, raw_password):
        """教員のパスワードをハッシュ化して保存"""
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        """パスワードを検証"""
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.teacher_name


# 試験情報
class Test(models.Model):
    test_id = models.AutoField(primary_key=True)  # 自動インクリメントに変更
    test_name = models.CharField(max_length=20)
    teacher_id = models.CharField(max_length=10)

# エラーログ
class ErrorLog(models.Model):
    error_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    error_message = models.TextField(max_length=200)
    timestamp = models.DateTimeField()
    
    def __str__(self):
        return f"Error {self.error_id}: {self.error_message}"

# アクションログ
class ActionLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} - {self.action} - {self.timestamp}"

# 2段階認証
class AuthTokens(models.Model):
    token_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    token = models.CharField(max_length=20)
    created_at = models.DateTimeField()
    expires_at = models.DateTimeField()

# ユーザープロフィール
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    student_id = models.CharField(max_length=20, unique=True, blank=True, null=True)  # 学籍番号
    grade = models.IntegerField(blank=True, null=True)  # 学年
    class_name = models.CharField(max_length=50, blank=True, null=True)  # クラス名
    role = models.CharField(max_length=20, choices=(
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ), default='student')

    def __str__(self):
        return f"{self.user.username} - {self.role}"

#自動採点関連
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
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions', default=1)  # 試験との紐付け
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

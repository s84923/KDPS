from django.db import models

# 生徒情報
class Student(models.Model):
    student_id = models.IntegerField(primary_key=True)
    student_name = models.CharField(max_length=20)
    school_year = models.IntegerField()
    student_class = models.CharField(max_length=3)
    email = models.CharField(max_length=30)
    parent_email = models.CharField(max_length=30)
    address = models.CharField(max_length=30)

# 成績情報
class Grades(models.Model):
    test_id = models.IntegerField()
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.IntegerField()
    answer_image = models.BinaryField()

# ユーザー情報
class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    teacher_id = models.CharField(max_length=10, null=True, blank=True)
    password = models.CharField(max_length=12)
    authority = models.IntegerField()

# 教員情報
class Teacher(models.Model):
    teacher_id = models.CharField(max_length=10, primary_key=True)
    teacher_name = models.CharField(max_length=20)
    school_year = models.IntegerField()
    student_class = models.CharField(max_length=3)
    post = models.CharField(max_length=10)

# 試験情報
class Test(models.Model):
    test_id = models.IntegerField(primary_key=True)
    test_name = models.CharField(max_length=20)
    teacher_id = models.CharField(max_length=10)

# エラーログ
class ErrorLog(models.Model):
    error_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    error_message = models.TextField(max_length=200)
    timestamp = models.DateTimeField()

# アクションログ
class ActionLog(models.Model):
    log_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField()

# 2段階認証
class AuthTokens(models.Model):
    token_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    token = models.CharField(max_length=20)
    created_at = models.DateTimeField()
    expires_at = models.DateTimeField()

# ユーザープロフィール
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, verbose_name="学籍番号")
    grade = models.PositiveIntegerField(verbose_name="学年")
    class_name = models.CharField(max_length=50, verbose_name="クラス")

    def __str__(self):
        return f'{self.user.username}のプロフィール'
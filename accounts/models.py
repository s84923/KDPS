# accounts/models.py
from django.db import models
from django.contrib.auth.models import User

# ユーザープロフィールモデル
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, verbose_name="学籍番号")
    grade = models.PositiveIntegerField(verbose_name="学年")
    class_name = models.CharField(max_length=50, verbose_name="クラス")

    def __str__(self):
        return f'{self.user.username}のプロフィール'

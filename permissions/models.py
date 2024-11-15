# models.py
from django.db import models

class UserRole(models.Model):
    name = models.CharField(max_length=100)
    admin_id = models.CharField(max_length=50)
    role = models.CharField(max_length=50)  # 役職 (教師, 生徒など)

    def __str__(self):
        return self.name

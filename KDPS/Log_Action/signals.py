# signals.py
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from KDPS.models import ActionLog

@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    ActionLog.objects.create(user_id=user.id, action="ログインしました")

@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    ActionLog.objects.create(user_id=user.id, action="ログアウトしました")

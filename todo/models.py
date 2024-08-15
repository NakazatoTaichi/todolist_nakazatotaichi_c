from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField('メールアドレス', unique=True)

class Task(models.Model):
    TASK_STATUS = [
        ('not_started', '未完了'),
        ('completed', '完了'),
    ]

    title = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=TASK_STATUS, default='not_started')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    due_date = models.DateTimeField()
    memo = models.TextField(default='詳細なし')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

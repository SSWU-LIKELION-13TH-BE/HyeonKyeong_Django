from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    nickname = models.CharField(max_length=50, blank=True, null=True)  # 닉네임 필드 추가

    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions_set", blank=True)

class User(models.Model):
    title = models.CharField(max_length=20, null = True)
    content = models.TextField()
    writer = models.CharField(max_length=20, null=True)
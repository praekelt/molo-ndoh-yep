from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", primary_key=True)
    date_of_birth = models.DateField()
    alias = models.CharField(
        max_length=128,
        blank=True,
        null=True)
    avatar = models.ImageField(
        'avatar',
        max_length=100,
        upload_to='users/profile',
        blank=True,
        null=True)

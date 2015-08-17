from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from datetime import datetime


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", primary_key=True)
    date_of_birth = models.DateField(null=True)
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

    def get_age(self):
        age = ''
        age_range = ''
        if self.date_of_birth:
            birth_date = datetime.strptime(str(self.date_of_birth), '%Y-%m-%d')
            age = ((datetime.today() - birth_date).days / 365)
            if age < 10:
                age_range = '0-9'
            elif age >= 10 and age <= 14:
                age_range = '10-14'
            elif age >= 15 and age <= 19:
                age_range = '15-19'
            elif age >= 20 and age <= 24:
                age_range = '20-24'
            elif age >= 25:
                age_range = '25+'
        return {'age': age, 'age_range': age_range}


@receiver(post_save, sender=User)
def user_profile_handler(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile(user=instance)
        profile.save()

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def copy_existing_user_profiles(apps, schema_editor):
    OldUserProfile = apps.get_model("app", "UserProfile")  # noqa
    UserProfile = apps.get_model("profiles", "UserProfile")  # noqa

    for old_profile in OldUserProfile.objects.all():
        profile, _ = UserProfile.objects.get_or_create(user=old_profile.user)
        profile.date_of_birth = old_profile.date_of_birth
        profile.alias = old_profile.alias
        profile.avatar = old_profile.avatar
        profile.save()


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20151105_1300'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(copy_existing_user_profiles),
    ]

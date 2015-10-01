from django.conf import settings

from app.forms import EditProfileForm, RegistrationForm
from app.models import UserProfile


def get_profile_data(request):
    username = ''
    alias = ''
    date_of_birth = ''
    if request.user.is_authenticated():
        user = request.user
        profile, _ = UserProfile.objects.get_or_create(user=user)
        username = user.username
        if profile.alias:
            alias = profile.alias
        else:
            alias = 'Anonymous'
        date_of_birth = profile.date_of_birth
    edit_profile_form = EditProfileForm(
        initial={
            'username': username,
            'alias': alias,
            'date_of_birth': date_of_birth
        }
    )
    registration_form = RegistrationForm()
    return {
        'username': username,
        'alias': alias,
        'date_of_birth': date_of_birth,
        'edit_profile_form': edit_profile_form,
        'registration_form': registration_form
    }


def get_registration_open(request):
    return {'REGISTRATION_OPEN': settings.REGISTRATION_OPEN}


def get_comment_open(request):
    return {'COMMENT_OPEN': settings.COMMENT_OPEN}

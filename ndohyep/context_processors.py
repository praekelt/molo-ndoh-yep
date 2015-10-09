from django.conf import settings
from molo.profiles.forms import RegistrationForm
from molo.profiles.forms import EditProfileForm, ProfilePasswordChangeForm


def default_forms(request):
    return {
        'registration_form': RegistrationForm(),
        'edit_profile_form': EditProfileForm(),
        'password_change_form': ProfilePasswordChangeForm()
    }


def get_registration_open(request):
    return {'REGISTRATION_OPEN': settings.REGISTRATION_OPEN}

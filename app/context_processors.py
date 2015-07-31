from app.forms import EditProfileForm
from app.models import UserProfile


def get_profile_data(request):
    username = ''
    alias = ''
    date_of_birth = ''
    if request.user.is_authenticated():
        try:
            user = request.user
            profile = user.profile
            username = user.username
            if profile.alias:
                alias = profile.alias
            else:
                alias = 'Anonymous'
            date_of_birth = profile.date_of_birth
        except UserProfile.DoesNotExist:
            pass
    edit_profile_form = EditProfileForm(
        initial={
            'username': username,
            'alias': alias,
            'date_of_birth': date_of_birth
        }
    )
    return {
        'username': username,
        'alias': alias,
        'date_of_birth': date_of_birth,
        'edit_profile_form': edit_profile_form
    }

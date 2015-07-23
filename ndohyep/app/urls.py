from app.views import logout_page, register, register_success
from app.views import MyProfileView, MyProfileEdit
from app.views import ProfilePasswordChangeView
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
# from django.conf import settings

urlpatterns = patterns(
    '',
    url(r'^logout/$', logout_page, name='auth_logout'),
    # If user is not login it will redirect to login page
    url(r'^login/$', 'django.contrib.auth.views.login', name='auth_login'),
    url(r'^register/$', register, name='user_register'),
    url(r'^register/success/$', register_success),
    url(
        r'^view/myprofile/$',
        login_required(MyProfileView.as_view()),
        name='view_my_profile'
    ),
    url(
        r'^edit/myprofile/$',
        login_required(MyProfileEdit.as_view()),
        name='edit_my_profile'
    ),
    url(
        r'^password-reset/$',
        login_required(ProfilePasswordChangeView.as_view()),
        name="profile_password_change"
    ),
)

from app.views import *
from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    url(r'^logout/$', logout_page, name='auth_logout'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='auth_login'), # If user is not login it will redirect to login page
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
	)

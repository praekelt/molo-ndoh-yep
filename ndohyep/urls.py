from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls

from ndohyep.views import CommentReplyFormView, search, report_response

from django.contrib.auth.decorators import login_required
from molo.profiles.views import RegistrationDone
from ndohyep.forms import DateOfBirthForm

urlpatterns = patterns(
    '',
    url(r'^django-admin/', include(admin.site.urls)),
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^polls/', include('polls.urls')),
    url(r'^surveys/', include('surveys.urls')),
    url(r'commenting/', include('molo.commenting.urls')),
    url(r'commenting/reply/(?P<parent_id>\d+)/$',
        CommentReplyFormView.as_view(),
        name='comments-reply'),
    url(r'^comments/reported/(?P<comment_pk>\d+)/$',
        report_response, name='report_response'),
    url(r'search/$', search, name='search'),
    url(r'^djga/', include('google_analytics.urls')),
    url(r'', include('molo.core.urls')),
    url(
        r'^profiles/register/done/',
        login_required(RegistrationDone.as_view(
            template_name="profiles/done.html",
            form_class=DateOfBirthForm
        )),
        name='registration_done'
    ),
    url(r'^profiles/', include('molo.profiles.urls',
                               namespace='molo.profiles')),
    url(r'', include(wagtail_urls)),
)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

from django.test import TestCase, RequestFactory

from ndohyep.context_processors import default_forms

from molo.profiles.forms import RegistrationForm
from molo.profiles.forms import EditProfileForm, ProfilePasswordChangeForm

from wagtail.wagtailcore.models import Site, Page
from django.contrib.contenttypes.models import ContentType
from molo.core.models import Main


class ContextProcessorsTest(TestCase):

    def setUp(self):
        # Create page content type
        page_content_type, created = ContentType.objects.get_or_create(
            model='page',
            app_label='wagtailcore'
        )

        # Create root page
        Page.objects.create(
            title="Root",
            slug='root',
            content_type=page_content_type,
            path='0001',
            depth=1,
            numchild=1,
            url_path='/',
        )

        main_content_type, created = ContentType.objects.get_or_create(
            model='main', app_label='core')

        # Create a new homepage
        self.main = Main.objects.create(
            title="Main",
            slug='main',
            content_type=main_content_type,
            path='00010001',
            depth=2,
            numchild=0,
            url_path='/home/',
        )
        self.main.save_revision().publish()

        # Create a site with the new homepage set as the root
        Site.objects.all().delete()
        self.site = Site.objects.create(
            hostname='localhost', root_page=self.main, is_default_site=True)
        self.factory = RequestFactory()

    def test_default_forms(self):
        request = self.factory.get('/profiles/register/')
        result = default_forms(request)
        self.assertTrue(
            isinstance(result['registration_form'], RegistrationForm))
        request = self.factory.get('/profiles/edit/myprofile/')
        result = default_forms(request)
        self.assertTrue(
            isinstance(result['edit_profile_form'], EditProfileForm))
        request = self.factory.get('/profiles/password-reset/')
        result = default_forms(request)
        self.assertTrue(isinstance(result['password_change_form'],
                        ProfilePasswordChangeForm))

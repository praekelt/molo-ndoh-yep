
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from wagtail.wagtailcore.models import Site, Page, Collection
from django.contrib.contenttypes.models import ContentType
from molo.core.models import Main


class UserProfileValidationTests(TestCase):
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

        # Create root collection
        Collection.objects.create(
            name="Root",
            path='0001',
            depth=1,
            numchild=0,
        )

        # Create a site with the new homepage set as the root
        Site.objects.all().delete()
        self.site = Site.objects.create(
            hostname='localhost', root_page=self.main, is_default_site=True)
        self.client = Client()

    def test_user_profile_validation(self):

        response = self.client.post(reverse('molo.profiles:user_register'), {
            'username': 'wrong username',
            'password': '1234',
        })
        self.assertContains(response,
                            'This value must contain only letters, '
                            'numbers and underscores.')

        response = self.client.post(reverse('molo.profiles:user_register'), {
            'username': 'username',
            'password': 'wrong',
        })
        self.assertContains(response,
                            'This value must contain only numbers.')

        response = self.client.post(reverse('molo.profiles:user_register'), {
            'username': 'username',
            'password': '12',
        })
        self.assertContains(response,
                            'Ensure this value has at least 4 characters'
                            ' (it has 2).')

        self.user = User.objects.create_user(
            username='tester',
            password='1234')

        response = self.client.post(reverse('molo.profiles:auth_login'), {
            'username': 'wrong',
            'password': '1234',
        })
        self.assertContains(response,
                            'Your username and password does not match.'
                            ' Please try again.')

        response = self.client.post(reverse('molo.profiles:auth_login'), {
            'username': 'tester',
            'password': 'wrong',
        })
        self.assertContains(response,
                            'Your username and password does not match.'
                            ' Please try again.')

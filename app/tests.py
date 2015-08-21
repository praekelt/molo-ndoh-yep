from datetime import date

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings

from wagtail.wagtailsearch.backends import get_search_backend

from app.forms import RegistrationForm, ProfilePasswordChangeForm

from molo.core.models import ArticlePage, SectionPage, Page


class RegisterTestCase(TestCase):

    def test_register_username_correct(self):
        form_data = {
            'username': 'Jeyabal@-1',
            'password': '1234',
            'date_of_birth': '1989-03-10',
        }
        form = RegistrationForm(data=form_data)
        self.assertEqual(form.is_valid(), True)

    def test_register_username_incorrect(self):
        form_data = {
            'username': 'Jeyabal#',
            'password': '1234',
            'date_of_birth': '1989-03-10',
        }
        form = RegistrationForm(data=form_data)
        self.assertEqual(form.is_valid(), False)

    def test_register_password_incorrect(self):
        form_data = {
            'username': 'Jeyabal#',
            'password': '12345',
            'date_of_birth': '1989-03-10',
        }
        form = RegistrationForm(data=form_data)
        self.assertEqual(form.is_valid(), False)

    def test_password_change_incorrect(self):
        form_data = {
            'old_password': '123',
            'new_password': 'jey123',
            'confirm_password': 'jey123',
        }
        form = ProfilePasswordChangeForm(data=form_data)
        self.assertEqual(form.is_valid(), False)

    def test_password_change_correct(self):
        form_data = {
            'old_password': '1234',
            'new_password': '3456',
            'confirm_password': '3456',
        }
        form = ProfilePasswordChangeForm(data=form_data)
        self.assertEqual(form.is_valid(), True)

    @override_settings(REGISTRATION_OPEN=True)
    def test_register_sets_dob(self):
        client = Client()
        response = client.post(reverse('user_register'), {
            'username': 'testing',
            'password': '1234',
            'date_of_birth': '1980-01-01',
        })
        self.assertRedirects(response, '/')
        user = User.objects.get(username='testing')
        self.assertEqual(user.profile.date_of_birth, date(1980, 1, 1))

    @override_settings(REGISTRATION_OPEN=True)
    def test_register_auto_login(self):
        client = Client()
        response = client.post(reverse('user_register'), {
            'username': 'testing',
            'password': '1234',
            'date_of_birth': '1980-01-01',
        })
        response = client.get('/')
        self.assertNotContains(response, 'Join the community!')

    @override_settings(REGISTRATION_OPEN=True)
    def test_registration_open(self):
        client = Client()
        response = client.get('/')
        self.assertNotContains(response, 'Registration is currently closed')

        response = client.get(reverse('user_register'))
        self.assertNotContains(response, 'Registration is currently closed')

        response = client.post(reverse('user_register'), {
            'username': 'testing',
            'password': '1234',
            'date_of_birth': '1980-01-01',
        })

        response = client.get('/')
        self.assertNotContains(response, 'Join the community!')

    @override_settings(REGISTRATION_OPEN=False)
    def test_registration_closed(self):
        client = Client()
        response = client.get('/')
        self.assertContains(response, 'Registration is currently closed')
        response = client.get(reverse('user_register'))
        self.assertContains(response, 'Registration is currently closed')

        response = client.post(reverse('user_register'), {
            'username': 'testing',
            'password': '1234',
            'date_of_birth': '1980-01-01',
        })
        response = client.get('/')
        self.assertContains(response, 'Registration is currently closed')


class TestSearch(TestCase):

    def test_search(self):
        for a in range(0, 20):
            ArticlePage.objects.create(
                title='article %s' % (a,), depth=a,
                subtitle='article %s subtitle' % (a,),
                slug='article-%s' % (a,), path=[a])

        self.backend = get_search_backend('default')
        self.backend.refresh_index()

        client = Client()
        response = client.get(reverse('search'), {
            'q': 'article'
        })

        self.assertContains(response, 'Page 1 of 2')
        self.assertContains(response, '&rarr;')
        self.assertNotContains(response, '&larr;')

        response = client.get(reverse('search'), {
            'q': 'article',
            'p': '2',
        })
        self.assertContains(response, 'Page 2 of 2')
        self.assertNotContains(response, '&rarr;')
        self.assertContains(response, '&larr;')


class TestCommentOpen(TestCase):
    #

    @override_settings(COMMENT_OPEN=True)
    def test_comment_open(self):
        client = Client()
        response = client.get('/')

        self.assertContains(response, 'comment_count')

    @override_settings(COMMENT_OPEN=False)
    def test_comment_close(self):
        client = Client()
        response = client.get('/')
        self.assertNotContains(response, 'comment_count')

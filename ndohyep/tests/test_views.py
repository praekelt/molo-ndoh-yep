import json
from datetime import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test.client import Client

from molo.core.models import ArticlePage, SectionPage
from molo.commenting.models import MoloComment
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site as DjangoSite
from wagtail.wagtailcore.models import Site, Page
from molo.core.models import Main
from django.contrib.auth.models import User, Group


class ViewsTestCase(TestCase):

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
        self.client = Client()
        self.user = User.objects.create_user(
            username='tester',
            email='tester@example.com',
            password='tester')

    def test_default_dob_in_registration_done(self):
        client = Client()
        client.login(username='tester', password='tester')
        response = client.get(reverse('registration_done'))

        year_25_ago = datetime.today().year - 25
        self.assertContains(
            response,
            '<option value="%(year)s" selected="selected">%(year)s</option>' %
            {'year': year_25_ago})

    def test_markdown_in_lists(self):
        section = SectionPage(
            title='Test Section', depth=3, slug='section')
        self.main.add_child(instance=section)
        section.save_revision().publish()
        article = ArticlePage(
            title='article 1', depth=1, subtitle='article 1 subtitle',
            slug='article-1', path=[1],
            body=json.dumps([
                {'type': 'list',
                 'value': ["Lorem *ipsum*"]},
                {'type': 'numbered_list',
                 'value': ["*sit* met"]}
            ]))
        section.add_child(instance=article)
        article.save_revision().publish()

        response = self.client.get("/section/article-1/")
        self.assertContains(
            response, "<li>Lorem <em>ipsum</em></li>")
        self.assertContains(
            response, "<li><em>sit</em> met</li>")


class TestReportResponse(TestCase):

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
        self.client = Client()
        self.user = User.objects.create_user(
            username='tester',
            email='tester@example.com',
            password='tester')

    def test_report_response(self):
        client = Client()
        article = ArticlePage.objects.create(
            title='article 1', depth=1,
            subtitle='article 1 subtitle',
            slug='article-1', path=[1])
        comment = MoloComment.objects.create(
            content_object=article, object_pk=article.id,
            content_type=ContentType.objects.get_for_model(article),
            site=DjangoSite.objects.get_current(), user=self.user,
            comment='comment 1', submit_date=datetime.now())
        response = client.get(reverse('report_response',
                                      args=(comment.id,)))
        self.assertContains(
            response,
            "This comment has been reported."
        )

    def test_markdown(self):
        group = Group(name="Experts")
        group.save()
        self.user.groups.add(group)

        section = SectionPage(
            title='Test Section', depth=3, slug='section')
        self.main.add_child(instance=section)
        section.save_revision().publish()
        article = ArticlePage(
            title='article 1', depth=1, subtitle='article 1 subtitle',
            slug='article-1', path=[1],
            body=json.dumps([
                {'type': 'list',
                 'value': ["Lorem *ipsum*"]},
                {'type': 'numbered_list',
                 'value': ["*sit* met"]}
            ]))
        section.add_child(instance=article)
        article.save_revision().publish()
        MoloComment.objects.create(
            content_object=article, object_pk=article.id,
            content_type=ContentType.objects.get_for_model(article),
            site=DjangoSite.objects.get_current(), user=self.user,
            comment='Click [here](http://google.com)',
            submit_date=datetime.now())

        response = self.client.get("/section/article-1/")
        self.assertContains(
            response, '<a href="http://google.com">here</a>')

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client

from wagtail.wagtailsearch.backends import get_search_backend

from molo.core.models import ArticlePage
from wagtail.wagtailcore.models import Site, Page, Collection
from django.contrib.contenttypes.models import ContentType
from molo.core.models import Main


class TestSearch(TestCase):
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

    def test_search(self):
        self.backend = get_search_backend('default')
        self.backend.reset_index()

        for a in range(0, 20):
            ArticlePage.objects.create(
                title='article %s' % (a,), depth=a,
                subtitle='article %s subtitle' % (a,),
                slug='article-%s' % (a,), path=[a])

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

        response = client.get(reverse('search'), {
            'q': 'article',
            'p': 'foo',
        })
        self.assertContains(response, 'Page 1 of 2')

        response = client.get(reverse('search'), {
            'q': 'article',
            'p': '4',
        })
        self.assertContains(response, 'Page 2 of 2')

        response = client.get(reverse('search'), {
            'q': 'magic'
        })
        self.assertContains(response, 'No search results for magic')

        response = client.get(reverse('search'))
        self.assertContains(response, 'No search results for None')

from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailsearch import index

from molo.core.models import HomePage

HomePage.subpage_types += ['polls.Question']


class Question(Page):
    parent_page_types = [
        'core.HomePage', 'core.SectionPage', 'core.ArticlePage']
    subpage_types = ['polls.Choice']


class Choice(Page):
    votes = models.IntegerField(default=0)

    promote_panels = Page.promote_panels + [
        FieldPanel('votes'),
    ]

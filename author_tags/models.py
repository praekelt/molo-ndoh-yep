from django.db import models
from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel

from molo.core.models import ArticlePage

ArticlePage.subpage_types += ['author_tags.Authortags']

AGE_RANGE_CHOICES = (
    ('All', 'All'),
    ('10-14', '10-14'),
    ('15-19', '15-19'),
    ('20-24', '20-24'),
    ('25+', '25+'),
)


class Authortags(Page):
    parent_page_types = ['core.ArticlePage']
    age_range_tags = models.CharField(
        max_length=10,
        choices=AGE_RANGE_CHOICES,
        default=0,
        null=True,
        blank=True
    )

Authortags.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('age_range_tags')
]

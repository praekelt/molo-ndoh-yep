from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel

from molo.core.models import ArticlePage

ArticlePage.subpage_types += ['author_tags.Authortags']


class Authortags(Page):
    parent_page_types = ['core.ArticlePage']


Authortags.content_panels = [
    FieldPanel('title', classname='full title'),
]

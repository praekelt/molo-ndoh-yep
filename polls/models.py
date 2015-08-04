from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailsearch import index

from molo.core.models import LanguagePage


class LanguagePage(LanguagePage):
    LanguagePage.subpage_types = [
        'core.HomePage',
        'core.SectionPage',
        'core.FooterPage',
        'polls.Question',
        'surveys.Survey'
    ]


class Question(Page):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_("Choose Page")
    )

    def __str__(self):
        return self.question_text

    search_fields = Page.search_fields + (
        index.SearchField('pub_date'),
        index.SearchField('question_text'),
    )

    content_panels = Page.content_panels + [
        FieldPanel('page'),
        FieldPanel('pub_date'),
        FieldPanel('question_text'),
    ]
    subpage_types = ['polls.Choice']


class Choice(Page):
    question = models.ForeignKey(
        Question,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    search_fields = Page.search_fields + (
        index.SearchField('choice_text'),
    )

    content_panels = Page.content_panels + [
        FieldPanel('question'),
        FieldPanel('choice_text'),
        FieldPanel('votes'),
    ]


from copy import copy

from django import template

from surveys.models import Survey

register = template.Library()


@register.inclusion_tag('surveys/survey_page.html',
                        takes_context=True)
def survey_page(context, pk=None, page=None):
    context = copy(context)
    questions = Survey.objects.filter(page=page.id)
    if questions:
        context.update({
            'questions': questions
        })
    else:
        context.update({
            'error': True,
        })
    return context

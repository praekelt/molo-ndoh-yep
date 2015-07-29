
from copy import copy

from django import template

from polls.models import Question

register = template.Library()


@register.inclusion_tag('polls/poll_page.html',
                        takes_context=True)
def poll_page(context, pk=None, page=None):
    context = copy(context)
    polls = Question.objects.filter(page=page.id)
    if polls:
        context.update({
            'questions': polls
        })
    else:
        context.update({
            'error': True,
        })
    return context

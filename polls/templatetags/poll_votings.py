
from copy import copy

from django import template

from polls.models import Question

register = template.Library()


@register.inclusion_tag('polls/poll_page.html',
                        takes_context=True)
def poll_page(context, pk=None, page=None):
    context = copy(context)
    if page:
        questions = Question.objects.live().child_of(page)
        context.update({
            'questions': questions
        })
    return context

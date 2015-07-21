
from copy import copy

from django import template

from polls.models import Choice, Question

register = template.Library()

@register.inclusion_tag('polls/poll_widget.html',
                        takes_context=True)
def poll_widget(context, pk=None):
    context = copy(context)
    try:
        polls = Question.objects.order_by('-pub_date')[:5]
    except Question.DoesNotExist:
        context.update({
            'error': True,
        })
    context.update({
        'latest_question_list': polls
    })
    return context


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
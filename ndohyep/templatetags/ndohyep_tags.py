from django import template
from django.utils.safestring import mark_safe
from markdown import markdown

register = template.Library()


def is_in_group(user, group_name):
    """
    Check if a user in a group named ``group_name``.

    :param user User:
        The auth.User object
    :param group_name str:
        The name of the group
    :returns: bool
    """
    return user.groups.filter(name__exact=group_name).exists()


def handle_markdown(value):
    md = markdown(
        value,
        [
            'markdown.extensions.fenced_code',
            'codehilite',
        ]
    )
    return mark_safe(md)

register.filter('is_in_group', is_in_group)
register.filter('handle_markdown', handle_markdown)

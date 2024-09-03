from django import template

register = template.Library()
@register.filter
def custom_range(value):
    return range(value+1)
@register.simple_tag
def status_range():
    return ['Unwatched', 'Watching', 'Completed','On-Hold','Dropped','Plan to Watch']

@register.simple_tag
def status_range2():
    return ['Unread', 'Reading', 'Completed','On Hold','Dropped','Plan to Read']
from django import template
from django.utils import timezone
from django.utils.timesince import timesince

register = template.Library()

@register.filter
def smart_timestamp(date):
    now = timezone.now()
    diff = now - date

    if diff.days < 1:
        return f"{timesince(date)} ago"
    return date.strftime("%Y-%m-%d %H:%M")

from django import template
from ..renderers import DateTimePicker


register = template.Library()

@register.simple_tag
def datetime_picker(field, *args, **kwargs):
    return DateTimePicker(field, *args, **kwargs).render()

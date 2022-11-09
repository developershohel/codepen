from django import template

register = template.Library()


@register.simple_tag()
def file_ext(value):
    return value.strip('.').pop()

import re

from django import template
from django.template.defaultfilters import stringfilter
from django.urls import reverse

from pen.models import Pen

register = template.Library()


@register.filter('filter_by_id')
def filter_by_id(value, field):
    db_filter = value.filter(id=field)
    if db_filter:
        return db_filter
    else:
        return value


@register.filter('count_by_id')
def db_count_by_id(value, field):
    db_filter = value.filter(id=field)
    if db_filter:
        return db_filter.count()
    else:
        return value


@register.filter('filter_by_user_id')
def filter_by_user_id(value, field):
    db_filter = value.filter(user_id=field)
    if db_filter:
        return db_filter
    else:
        return value


@register.filter('count_by_user_id')
def filter_by_user_id(value, field):
    db_filter = value.filter(user_id=field)
    if db_filter:
        return db_filter.count()
    else:
        return value


@register.filter('filter_by_pen_id')
def filter_by_pen_id(value, field):
    val = value.filter(pen_id=field)
    if val:
        return val
    else:
        return value


@register.filter('count_by_pen_id')
def count_by_pen_id(value, field):
    val = value.filter(pen_id=field)
    if val:
        return val.count()
    else:
        return value


@register.filter('word_slice')
@stringfilter
def word_slice(value, number):
    total_world = value.split()
    bits = []
    for x in str(number).split(":"):
        if not x:
            bits.append(None)
        else:
            bits.append(int(x))
    slice_word = total_world[slice(*bits)]
    return ' '.join(slice_word)


@register.filter('word_count')
@stringfilter
def word_count(value):
    total_world = value.split()
    return len(total_world)


@register.filter('file_ext')
@stringfilter
def file_ext(value):
    file_name = str(value)
    file_extension = f".{file_name.split('.').pop()}"
    return file_extension


@register.filter('strip_filename')
@stringfilter
def strip_filename(value):
    filename_count = len(value)
    if filename_count > 25:
        get_file_ext = file_ext(value)
        return f'{value[0:25]}....{get_file_ext}'
    else:
        return value


@register.filter('split_text')
@stringfilter
def split_text(value, args=None):
    if isinstance(value, str) and args and len(args.split(':')) <= 3:
        if args:
            args_len = args.split(':')
            if len(args_len) == 1:
                seperator = args_len[0]
                split_value = value.split(seperator)
                return split_value
            elif len(args_len) == 2:
                seperator = args_len[0]
                split_value = value.split(seperator)[int(args_len[1])]
                return split_value
            elif len(args_len) == 3:
                seperator = args_len[0]
                split_value = value.split(seperator)[int(args_len[1]):int(args_len[2])]
                return split_value
        else:
            return value.split()
    else:
        return value


@register.filter('value_type')
@stringfilter
def value_type(value):
    return type(value)


@register.filter('create_list')
@stringfilter
def create_list(value):
    if isinstance(value, list):
        return value
    elif re.split(r'\s', value):
        return value.split(' ')
    else:
        new_val = [value]
        return new_val


@register.filter('capitalize')
def capitalize(value):
    return value.capitalize()


@register.filter('convert_string')
def convert_string(value):
    if isinstance(value, list) or isinstance(value, tuple):
        new_val = []
        for i in value:
            new_val.append(str(i))
        return new_val
    else:
        return str(value)


@register.filter('lstrip')
@stringfilter
def lstrip(value, args=None):
    if args:
        return value.lstrip(str(args))
    else:
        return value.lstrip(' ')


@register.filter('rstrip')
@stringfilter
def rstrip(value, args=None):
    if args:
        return value.rstrip(str(args))
    else:
        return value.rstrip(' ')


@register.simple_tag
def current_menu(request, current):
    current_path = reverse(current)
    if request == current_path:
        return 'current'
    else:
        return ''


@register.filter('trending_pen_filter')
def trending_pen_fileter(pen_id):
    if not int(pen_id):
        return pen_id
    pen = Pen.objects.all().filter(id=pen_id)

    if pen:
        return pen
    else:
        return pen_id
